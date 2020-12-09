import socket
import sys
req = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 1234))

s.send(b'')
data = s.recv(1000)
s.close()
