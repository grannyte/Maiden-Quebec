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


def _format_msg(msg):
    return bytes(msg, 'ascii')


def client_thread(conn):
    conn.send(b'Welcome to the server. Type something and hit enter\n')
    while True:
        reply = b'.' # always send something, so the client knows the connection is up and running
        data = conn.recv(1024)
        if not data:
            continue
        elif data == b':quit':
            break
        str_data = data.decode("ascii")
        if str_data.startswith('CONNECTING'):
            _, user, password = str_data.split(' ')
            # look up the database
            reply = _format_msg(user + ' has been successfully connected.')

        conn.sendall(reply)
    conn.close()


class Server():
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._bind_server('localhost', 9090)
        self._max_connections(3)

    def _bind_server(self, host, port):
        try:
            self.server.bind((host, port))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

    def _max_connections(self, max_connections):
        self.server.listen(max_connections)

    def run(self): 
        while True:
            conn, address = self.server.accept()
            ip, port = address[0], address[1]
            print('Connected with ' + ip + ':' + str(port))
            t = Thread(target=client_thread, args=(conn,))
            t.start()
        self.server.close()


if __name__ == "__main__":
    server = Server('localhost', 9090)
    server.run()