import socket
from datetime import datetime
import sys

def readDataFromFile(filename, address_dict):  # first start the program by
    # reading contents from ips.txt
    # file and insert them to the dictionary
    fp = open(filename, 'r')  # open file 'ips.txt' for reading first the addresses
    line = fp.readline()
    cnt = 1
    while line:  # go through each line in file and add to the dictionary the relevant stuff
        # print("Line {}: {}".format(cnt, line.strip()))
        x = line.split(",")
        arr_len = len(x)
        temp_list = []
        for i in x:
            temp = i.split('\n')  # strip the string from '\n'
            temp_list.append(temp[0])  # append the string after the comman to the list
        if (len(temp_list) == 3):
            temp_list.append("0")  # 'false' mean that its a static address that should never be forgotten
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            temp_list.append(timestamp)
        address_dict[temp_list[0]] = temp_list
        line = fp.readline()
        cnt += 1
    fp.close()

def conncetToFatherServer(filename, unknownAddr, parentip, parentport, address_dict):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.sendto(unknownAddr.encode(), (parentip, int(parentport)))
    data, addr = soc.recvfrom(1024)
    if not data:
        return "not found"
    if type(data) is list:
        tmp_list = []
        tmp_list.append(data[0])
        tmp_list.append(data[1])
        tmp_list.append(data[2])
        tmp_list.append('1')
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        tmp_list.append(timestamp)
        address_dict[tmp_list[0]] = tmp_list
        writeDataToFile(filename, address_dict)

    soc.close()
def writeDataToFile(filename, address_dict):# write date to file 'ips.txt'
    fp = open(filename, 'w')
    fp.truncate()
    for key in address_dict:
        my_list = address_dict[key]
        my_string = ""
        cnt = 0
        for j in my_list:
            if (cnt < len(my_list) - 1):
                my_string = my_string + j + ","
            cnt = cnt + 1
        fp.write('%s%s\n' % (my_string, j))  # write the value of the current key to the ips.txt file
    fp.close()

def FindAddressInDB(address_dict, input_address):
    empty_list = []
    for key in address_dict:
        if key == input_address:
            empty_list = address_dict[key]
            if(empty_list[3] == "1"):
                now = datetime.now()
                timestamp = datetime.timestamp(now)
                t1 = datetime.strptime(empty_list[4], "%b %d %H:%M:%S %Y")
                t2 = datetime.strptime(timestamp, "%b %d %H:%M:%S %Y")
                difference = t1 - t2
                if(difference.seconds <= int(empty_list[2])):
                    return address_dict[key]
                else:
                    deleteRecordFromFileDB(key, address_dict)
    return empty_list

def deleteRecordFromFileDB(linetodelete, address_dict):
    del address_dict[linetodelete]


def main():
    isFatherrelevant = 0
    address_dict = dict()  # initialize empty dictionary
    # to hold the addresses , ip and TTl of sites. key is the address and value is
    # list of the current line separated by comma
    myport = sys.argv[1]
    parentip = sys.argv[2]
    if(int(parentip) != -1):
        isFatherrelevant = 1
    parentport = sys.argv[3]
    filepath = sys.argv[4]
    readDataFromFile(filepath, address_dict)
    my_list = []
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(myport)))

    while True:
        print("waiting for client....")
        data, addr = s.recvfrom(1024)
        print("connection established, client's connection details:" + addr)
        print("client is searching for the ip of: %s, no problemo, searching....", data.decode())
        input_query = data.decode()
        my_list = FindAddressInDB(address_dict, input_query, isFatherrelevant)
        if not my_list:
            conncetToFatherServer(filepath, input_query, parentip, parentport, address_dict)
            my_list = FindAddressInDB(address_dict, input_query, isFatherrelevant)
        if not my_list:
            s.sendto(b'not found', addr)
        else:
            res = my_list[1]
            s.sendto(res.encode(), addr)


        #print(str(data), addr)
        #s.sendto(data.upper(), addr)


main()
