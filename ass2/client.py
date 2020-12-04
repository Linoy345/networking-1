import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('10.0.2.15', 12343))
s.send(b'linoy sela')
data = s.recv(100)
print("Server sent: ", data)

s.send(b'207654344')
data = s.recv(100)
print("Server sent: ", data)

s.close()
