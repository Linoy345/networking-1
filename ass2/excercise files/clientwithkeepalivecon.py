import socket
import sys
req = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 80))

s.send(b'GET index.html HTTP/1.1\r\nConnection: keep-alive\r\n\r\nGET index.html HTTP/1.1\r\nConnection: keep-alive\r\n\r\nGET index.html HTTP/1.1\r\nConnection: keep-alive\r\n\r\n')
data = s.recv(1000)
print(data.decode("utf-8"))
data = s.recv(1000)
print(data.decode("utf-8"))
data = s.recv(1000)
print(data.decode("utf-8"))
s.close()
