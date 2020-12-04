import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 1234))
s.send(b'linoy sela')
data = s.recv(100)
print("Server sent: ", data)

s.send(b'207654344')
data = s.recv(100)
print("Server sent: ", data)

s.close()
