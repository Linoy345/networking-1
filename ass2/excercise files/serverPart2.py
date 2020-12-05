import socket
import sys
import os


def proccess_client_request(conn, data):  # this is the main function - from here we start to proccess the message from client
    path = ""  # for now send empty string to check_if_file_exist in order to get not found message on browser
    #check_if_file_exist(conn, path)


def check_if_file_exist(conn, path, connection_status):
    files = "files/"
    path = files + path
    if (os.path.isfile(path) == False):  # send FileNotFound
        conn.send(b'HTTP/1.1 404 Not Found \r\n')
        conn.send(b'Connection: close \r\n')
        conn.send(b'\r\n')
        # need to close the connection and take care of new connection
        # conn.close() ??????

    else: #dont know how to read files especially hmt files
        f = open(path, 'rb')
        file_content = f.read()
        length = os.path.getsize(path) #????? שימו לב, length הוא כמות הבתים שנשלחים בפוע???#
        conn.send(b'HTTP/1.1 200 OK \r\n')
        conn.send(b'Connection: ' + connection_status.encode() + b'\r\n')
        conn.send(b'Content-Length: ' + str(length).encode() + b'\r\n')
        conn.send(b'\r\n') #empty line
        conn.send(file_content + b'\r\n')
        conn.send(b'\r\n')

        if connection_status == 'close' :
            #need to close the connection after sending the inforamtion and take care of new connection
            #conn.close()
            print("???")
        else : #keep alive
            #conection stay open and need to read the next req
            print("???")


def redirection(conn):
    conn.send(b'HTTP/1.1 301 Moved Permanently')
    conn.send(b'\r\n')
    conn.send(b'Connection: close')
    conn.send(b'\r\n')
    conn.send(b'Location:/result.html')
    conn.send(b'\r\n\r\n')


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
    #data = ""  # assign empty string, in the future it will carry the message from client
    myport = sys.argv[1]  # this variable will hold the port that the server will listen to
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', int(myport)))
    s.listen(5)

    while True:  # as long as the list is not empty, we wont close the socket
        conn, addr = s.accept()
        #one sec
        chr = conn.recv(1024)  # each time we check if the next char from client is \r\n\r\n
        print(chr.decode())
        req = chr.decode().split(sep="\r\n\r\n") #save all the requests
        dict = parse_information(req) #the key is the adress from get and the value is the connection status
        for i in dict.keys():
            if i == '' : #empty message from client, need to close and get another client
                print("???")
            if i == '/redirect':
                redirection(conn)
            else :
                check_if_file_exist(conn, i, dict.get(i))




main()
