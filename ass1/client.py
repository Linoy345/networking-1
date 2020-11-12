import socket
import sys
import json


def main():
    serverIP = sys.argv[1]
    serverPort = sys.argv[2]
    txt = []
    print("trying to cennect to server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        print("Type your web address and get its ip address: ")
        txt = input()
        s.sendto(txt.encode(), (serverIP, int(serverPort)))
        data, addr = s.recvfrom(1024)
        deserialized = json.loads(data.decode())
        if not deserialized:
            print("not found")
        else:
            print(deserialized[1])
    # s.close()


main()
