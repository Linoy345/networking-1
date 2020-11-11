import socket
import sys


def main():
    serverIP = sys.argv[1]
    serverPort = sys.argv[2]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        txt = input("Type your web address and get its ip address: ")
        s.sendto(txt.encode(), (serverIP, 1234))
        data, addr = s.recvfrom(1024)
        if type(data) is list:
            print(str(data[1]))
        else:
            print "not found"
    # s.close()


main()
