import socket
from datetime import datetime
import sys
import json


# funcion to deal with reading from file procedure
def readDataFromFile(filename, address_dict):  # first start the program by
    # reading contents from ips.txt
    # file and insert them to the dictionary
    fp = open(filename, 'r')  # open file given as argument for reading
    line = fp.readline()
    cnt = 1
    while line:  # go through each line in file and add to the address_dict list of lists
        # print("Line {}: {}".format(cnt, line.strip()))
        x = line.split(",")  # regex for extracting strings from line
        arr_len = len(x)
        temp_list = []
        for i in x:
            temp = i.split('\n')  # strip the string from '\n'
            temp_list.append(temp[0])  # append the string after the comman to the list
        if (len(temp_list) == 3):
            temp_list.append("0")  # '0' mean that its a static address that should never be forgotten
            # and '1' mean that its a dynamic thats needs to check the TTL everytime
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            temp_list.append(timestamp)
        address_dict.append(temp_list)  # add list to address_dict list of lists
        line = fp.readline()
        cnt += 1
    fp.close()


# function to deal with connection to father server and recieving relevant from it
def conncetToFatherServer(filename, unknownAddr, parentip, parentport, address_dict):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # from recitation with Hemi
    soc.sendto(unknownAddr.encode(), (parentip, int(parentport)))  # from recitation with Hemi
    data, addr = soc.recvfrom(1024)  # from recitation with Hemi
    deserialized = json.loads(data.decode())  # deserialize the binary string from socket
    if not deserialized:  # if the object is empty
        return "not found"
    if type(deserialized) is list:  # if the object is list
        tmp_list = []  # initialize new empty list and build it with the data from the list on father server
        tmp_list.append(deserialized[0])
        tmp_list.append(deserialized[1])
        tmp_list.append(deserialized[2])
        tmp_list.append('1')  # '0' mean that its a static address that should never be forgotten
        # and '1' mean that its a dynamic thats needs to check the TTL everytime
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        tmp_list.append(timestamp)
        address_dict.append(tmp_list)  # add the new list to DB
        writeDataToFile(filename, address_dict)  # rewrite the file according to changes in DB
    soc.close()


# function to deal with writing data to file according to DB
def writeDataToFile(filename, address_dict):  # write date to file 'ips.txt'
    fp = open(filename, 'w')
    fp.truncate()  # truncate the file, now i am rewriting everything
    for key in address_dict:  # iterate through DB and write in file
        my_list = key
        my_string = ""
        cnt = 0
        for j in my_list:
            if (cnt < len(my_list) - 1):
                my_string = my_string + j + ","
            cnt = cnt + 1
        fp.write('%s%s\n' % (my_string, j))  # write the value of the current key to the file
    fp.close()


# function to help searching the DB for specific data, and delete old data if neccessary
def FindAddressInDB(filename, address_dict, input_address):
    empty_list = []
    for key in address_dict:
        if key[0] == input_address:
            empty_list = key
            if (empty_list[3] == "1"):  # '0' mean that its a static address that should never be forgotten
                # and '1' mean that its a dynamic thats needs to check the TTL everytime
                now = datetime.now()
                timestamp = datetime.timestamp(now)
                t1 = datetime.fromtimestamp(float(empty_list[4]))
                t2 = datetime.fromtimestamp(timestamp)
                # a = datetime(t1)
                # b = datetime(t2)

                difference = (
                        t2 - t1).total_seconds()  # check if the TTL of dynamic address has passes, if so - delete it from DB else return the relevant data
                if difference <= int(empty_list[2]):
                    return key
                else:
                    deleteRecordFromFileDB(key, address_dict)
                    writeDataToFile(filename, address_dict)
                    return []
            else:
                return empty_list
    return empty_list


# function to help deleting specific data from DB
def deleteRecordFromFileDB(linetodelete, address_dict):
    j = 0
    for i in address_dict:
        if i[0] == linetodelete[0]:
            address_dict.remove(i)


def main():
    isFatherrelevant = 0  # checking if father server exists
    address_dict = []
    # to hold the addresses , ip and TTl of sites. key is the address and value is
    # list of the current line separated by comma
    myport = sys.argv[1]
    parentip = sys.argv[2]
    if parentip != "-1":
        isFatherrelevant = 1 # father server exists
    parentport = sys.argv[3]
    filepath = sys.argv[4]
    readDataFromFile(filepath, address_dict) #start program by initializing DB
    writeDataToFile(filepath, address_dict) #start program by rewriting the file with my additions
    my_list = []
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #from recitation
    s.bind(('', int(myport)))
    while True:
        print("waiting for client....")
        data, addr = s.recvfrom(1024)
        print("connection established")
        print("client is searching for the ip of:" + data.decode() + ", no problemo, searching....", )
        input_query = data.decode() #extract the string from socket
        my_list = FindAddressInDB(filepath, address_dict, input_query) #search for the input in DB
        if not my_list and isFatherrelevant == 1: #if input not exist in DB and father server exist,
            # ask the father server for help, maybe he has the data about the input
            conncetToFatherServer(filepath, input_query, parentip, parentport, address_dict) #connect to father server and ask for relevant data,
            # if we found one then add it to DB and rewrote file, if not then move on
            my_list = FindAddressInDB(filepath, address_dict, input_query) #search again the input in DB after asking father server for help
        serialized = json.dumps(my_list)
        s.sendto(serialized.encode(), addr)

main()
