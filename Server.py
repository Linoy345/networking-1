import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 12345))

while True:
    print("connection opened. waiting for client....")
    data, addr = s.recvfrom(1024)
    print("ack from client")
    print(str(data), addr)
    s.sendto(data.upper(), addr)
