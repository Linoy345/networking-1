import socket
import sys

#get from the user name
name = input("Enter internet adress: ")

#get ipserver and portserver as argumemts
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.sendto(b'biu.ac.il', ('10.0.2.15', 12345))
s.sendto(name.encode(),(sys.argv[1],int(sys.argv[2])))

data, addr = s.recvfrom(1024)
splitData = data.decode().split(",", 1)
print(splitData[0])
s.close()




