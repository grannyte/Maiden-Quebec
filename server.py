# -*- coding: utf-8 -*-
from __future__ import print_function
"""
    Game Server using threads to manage connections.  Server is using the TCP protocol and
    might not suit game over Internet.  It is best to host local network games.  As this game
    is a prototype, you are urged to not push it to his limit; keep the number of connections low.
"""
 
import socket
import sys
from threading import *


def client_thread(conn):
    conn.send(b'Welcome to the server. Type something and hit enter\n')
    while True:
        reply = b'.'
        data = conn.recv(1024)
        if not data:
            continue
        elif data == b':quit':
            break
        str_data = data.decode("ascii")
        if str_data.startswith('CONNECTING'):
            _, user, passwd = str_data.split(' ')
            # look up the database
            reply = _format_msg(user + ' has been successfully connected.')

        conn.sendall(reply)

    conn.close()

def _format_msg(msg):
    return bytes(msg, 'ascii')
 

def main():
    # Bind socket to local host and port
    host = 'localhost'
    port = 9090
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    max_connections = 3
    s.listen(max_connections)

    is_running = True
    while is_running:
        conn, address = s.accept()
        print('Connected with ' + address[0] + ':' + str(address[1]))

        t = Thread(target=client_thread, args=(conn,))
        t.start()

    s.close()

if __name__ == "__main__":
    main()