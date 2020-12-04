import socket
import sys
import os


def proccess_client_request(conn,
                            data):  # this is the main function - from here we start to proccess the message from client
    path = ""  # for now send empty string to check_if_file_exist in order to get not found message on browser
    check_if_file_exist(conn, path)


def check_if_file_exist(conn, path):
    data = ""
    if (os.path.isfile(path) == False):  # send FileNotFound
        conn.send(b'HTTP/1.1 404 Not Found')
        conn.send(b'\n')
        conn.send(b'Connection: close')
        conn.send(b'\r\n\r\n')
        # conn.close()
    else:#dont know how to read files especially hmt files

        conn.send(b'\r\n\r\n')


def redirection(conn):
    data = ""
    conn.send(b'HTTP/1.1 301 Moved Permanently')
    conn.send(b'\n')
    conn.send(b'Connection: close')
    conn.send(b'Location:/result.html')
    conn.send(b'\r\n\r\n')


def main():
    flag = 0
    path = "files/index.html"
    my_list = [1]
    data = ""  # assign empty string, in the future it will carry the message from client
    address_dict = {'BUFFERSIZE': 1,
                    'FOUNDFILECLOSECON': 'HTTP/1.1 200 OK\nConnection: close\nContent-Length:',
                    'FOUNDFILECONKEEPALIVE': 'HTTP/1.1 200 OK\nConnection: keep-alive\nContent-Length:',
                    'REDIRECT': 'HTTP/1.1 301 Moved Permanently\nConnection: close\nLocation:/result.html\n\n',
                    'NOTFOUND': 'HTTP/1.1 404 Not Found\nConnection: close\r\n'}
    myport = sys.argv[1]  # this variable will hold the port that the server will listen to
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', int(myport)))
    s.listen(1)

    while True:  # as long as the list is not empty, we wont close the socket
        conn, addr = s.accept()
        # while (flag == 0):
        chr = conn.recv(1024)  # each time we check if the next char from clien is \r\n\r\n
    # data = data + chr  # concat the last char with the rest of the string
    # if ((len(data) >= 4) and data[-4:-1] == "\r\n\r\n"):
    # proccess_client_request(conn, my_list, path,address_dict)  # the client finished the message, now we can proccess it,
    # redirection(conn,my_list,path,address_dict)
    # if the file not found or something else unusual we close the socket
    # if(not my_list) :
    # flag = 1
    # conn.send(data.upper())



main()
