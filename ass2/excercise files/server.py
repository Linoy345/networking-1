import socket
import sys
import os


# ________________________CONSTS_______________________#


HTTP_OK_STR = "HTTP/1.1 200 OK\r\n"
HTTP_MOVED_STR = "HTTP/1.1 301 Moved Permanently\r\n"
HTTP_NOT_FOUND_STR = "HTTP/1.1 404 Not Found\r\n"
CONNECTION_STR = "Connection: "
CONNECTION_CLOSE_STR = "Connection: close"
CONTENT_LEN_STR = "Content-Length: "
LOCATION_RESULT_STR = "Location: /result.html\r\n\r\n"
BUFFER_SIZE = 1024
SUFFIX = "\r\n\r\n"

def proccess_client_request(conn,
                            data):  # this is the main function - from here we start to proccess the message from client
    status = "open"
    req = data.split(sep="\r\n\r\n")  # save all the requests
    dictt = parse_information(req)  # the key is the adress from get and the value is the connection status
    for i in dictt.keys():
        if i == '':  # empty message from client, need to close and get another client
            status = 404
        if i == '/redirect':
            status = redirection(conn)
        else:
            status = check_if_file_exist(conn, i, dictt.get(i))
    return status

def read_send_bytes(conn, path):
    with open(path, "rb") as f:
        content = f.read(BUFFER_SIZE)
        while content:
            conn.send(content)
            content = f.read(BUFFER_SIZE)

def check_if_file_exist(conn, path, connection_status):
    files = "files/"
    path = files + path
    if (os.path.isfile(path) is False):  # send FileNotFound
        conn.send((HTTP_NOT_FOUND_STR + CONNECTION_CLOSE_STR + SUFFIX).encode())
        return 404 #close socket

    else:
        length = os.path.getsize(path)  # get size of the data in file
        conn.send((HTTP_OK_STR + CONNECTION_STR + connection_status + '\r\n' + CONTENT_LEN_STR +
                   str(length) + SUFFIX).encode())
        read_send_bytes(conn, path)
        if (connection_status == "close"):
            return 404 #close socket
        else:
            return 200 #keep socket alive


def redirection(conn):
    conn.send((HTTP_MOVED_STR + CONNECTION_CLOSE_STR + '\r\n' + LOCATION_RESULT_STR + SUFFIX).encode())
    path = "files/result.html"
    read_send_bytes(conn, path)
    return 404 #close socket


def parse_information(req):
    flag = 0
    list_gets = []  # all the get req
    list_cons = []  # all the status connection
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
    s.listen(1)
    chr = 'a'
    status = "open"  # by default we stay in keep-alive mode so we dont close the socket

    while True:
        conn, addr = s.accept()
        status = 200
        data = ""
        try:
            conn.settimeout(1)
            while chr and conn.fileno() != -1:  # flag will be turned on when we get '\r\n\r\n
                chr = conn.recv(1).decode()  # each time we check if the next char from client is \r\n\r\n
                if (not chr):  # client sent empty message
                    status = 404
                else:
                    data = data + chr
                    if (len(data) >= 4 and data[-4:] == '\r\n\r\n'):
                        print(data)
                        status = proccess_client_request(conn, data)
                        data = ""
                if (status == 404):  # we close the socket after the client sent empty message or wanted to close
                    conn.close()
            # if (status == 404):  # we close the socket after the client sent empty message or wanted to close
            #     conn.close()

        except socket.timeout:
            if (conn.fileno() != -1):
                conn.close()
        except :
            if (conn.fileno() != -1):
                conn.close()

main()
