import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b'Meni 204064257', ('172.16.22.60', 12345))
data, addr = s.recvfrom(1024)
print(str(data), addr)
s.close()
