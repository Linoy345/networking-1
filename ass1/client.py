import socket
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.sendto(b'Linoy Sela 207654344', ('10.0.2.15', 1234))
    data, addr = s.recvfrom(1024)
    print(str(data[1]))
#s.close()