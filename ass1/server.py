import socket
from datetime import datetime

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


# todo- add connection to father server
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


def deleteRecordFromFile(filename, linetodelete, address_dict):
    with open(filename, "r") as f:
        lines = f.readlines()
    with open(filename, "w") as f:
        for line in lines:
            if line.strip("\n") != linetodelete:
                f.write(line)


def main():
    address_dict = dict()  # initialize empty dictionary
    # to hold the addresses , ip and TTl of sites. key is the address and value is
    # list of the current line separated by comma
    filepath = 'ips.txt'
    readDataFromFile(filepath, address_dict)
    writeDataToFile(filepath, address_dict)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 1234))

    while True:
        print("waiting for client....")
        data, addr = s.recvfrom(1024)
        print("connection established, client's connection details:" + addr)

        print(str(data), addr)
        s.sendto(data.upper(), addr)


main()
