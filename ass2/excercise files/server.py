import socket
import sys
import os


def proccess_client_request(conn,
                            data):  # this is the main function - from here we start to proccess the message from client
    status = "open"
    req = data.split(sep="\r\n\r\n")  # save all the requests
    dictt = parse_information(req)  # the key is the adress from get and the value is the connection status
    for i in dictt.keys():
        if i == '':  # empty message from client, need to close and get another client
            status = "close"
        if i == '/redirect':
            status = redirection(conn)
        else:
            status = check_if_file_exist(conn, i, dictt.get(i))
    return status


def check_if_file_exist(conn, path, connection_status):
    files = "files/"
    path = files + path
    if (os.path.isfile(path) is False):  # send FileNotFound
        conn.send(b'HTTP/1.1 404 Not Found \r\n')
        conn.send(b'Connection: close \r\n')
        conn.send(b'\r\n')
        return connection_status.encode()

    else:
        f = open(path, 'rb')
        file_content = f.read()
        length = os.path.getsize(path)  # get size of the data in file
        conn.send(b'HTTP/1.1 200 OK \r\n'+b'Connection: ' + connection_status.encode() + b'\r\n'+
                  b'Content-Length: ' + str(length).encode() + b'\r\n\r\n')
        # conn.send(b'Connection: ' + connection_status.encode() + b'\r\n')
        # conn.send(b'Content-Length: ' + str(length).encode() + b'\r\n')
        # conn.send(b'\r\n')  # empty line
        conn.send(file_content + b'\r\n')
        # conn.send(b'\r\n')
        return connection_status.encode()


def redirection(conn):
    conn.send(b'HTTP/1.1 301 Moved Permanently')
    conn.send(b'\r\n')
    conn.send(b'Connection: close')
    conn.send(b'\r\n')
    conn.send(b'Location:/result.html')
    conn.send(b'\r\n\r\n')
    return "close"


def parse_information(req):
    flag = 0
    list_gets = []  # all the get req
    list_cons = []  # all the status conection
    d = {}
    for i in req:
        if 'GET ' in i:
            get = i.split('GET ')
            get = get[1]
            w_get = get.split()
            if (w_get[0] == '/'):
                w_get[0] = "index.html"  # if the adress is / means that its index.html
            list_gets.append(w_get[0])  # get the adress
            for j in w_get:
                if flag == 1:
                    list_cons.append(j)
                    flag = 0
                if 'Connection:' == j:
                    flag = 1
    for i in range(len(list_gets)):
        d.update({list_gets[i]: list_cons[i]})
    return d


def main():
    data = ""  # assign empty string, in the future it will carry the message from client
    myport = sys.argv[1]  # this variable will hold the port that the server will listen to
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', int(myport)))
    s.listen(5)
    chr = 'a'
    status = "open"  # by default we stay in keep-alive mode so we dont close the socket

    while True:
        conn, addr = s.accept()
        try:
            conn.settimeout(1)
            flag = 0
            while chr:  # flag will be turned on when we get '\r\n\r\n
                chr = conn.recv(1).decode()  # each time we check if the next char from client is \r\n\r\n
                if (not chr):  # client sent empty message
                    status = "close"
                else:
                    data = data + chr
                    if (len(data) >= 4 and data[-4:] == '\r\n\r\n'):
                        status = proccess_client_request(conn, data)
                        data = ""
                        if (status == "close"):
                            flag = 1

            if (status == "close"):  # we close the socket after the client sent empty message or wanted to close
                conn.close()
                flag = 0
        except socket.timeout:
            print("No Response")
            if (conn.fileno() != -1):
                conn.close()


main()
