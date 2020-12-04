import socket
import sys
import os




def main():
    address_dict = {}
    myport = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_SGRAM) #from recitation
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
