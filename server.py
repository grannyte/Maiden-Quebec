# -*- coding: utf-8 -*-
from __future__ import print_function
"""
    Game Server using threads to manage connections.  Server is using the TCP protocol and
    might not suit game over Internet.  It is best to host local network games.  As this game
    is a prototype, you are urged to not push it to his limit; keep the number of connections low.
"""

import threading
import socketserver
import datetime

from database_builder import DatabaseBuilder
from database import Database


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.db = Database()  # TODO: close database   with:  keyword
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        request = str(self.request.recv(1024), 'ascii').strip()
        response = b'.'
        if request.startswith('LOGIN'):
            _, user, password = request.split(' ')
            if self.db.query_is_connected(user):
                response = bytes("{} {}".format(user, 'is already connected.'), 'ascii')
            else:
                date_in = datetime.datetime.now(datetime.timezone.utc).timestamp()
                self.db.login(user, date_in)
                response = bytes("{} {}".format(user, 'has been successfully connected.'), 'ascii')
        elif request.startswith('LOGOUT'):
            _, user = request.split(' ')
            if self.db.query_is_connected(user):
                date_out = datetime.datetime.now(datetime.timezone.utc).timestamp()
                self.db.logout(user, date_out)
                response = bytes("{} {}".format(user, 'has been successfully disconnected.'), 'ascii')
            else:
                response = bytes("{}".format('Are you messing with the server ?'), 'ascii')
        elif request.startswith('ENTITIES'):
            # TODO: query the database
            _, zone = request.split(' ')
        self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Set up the database beforehand
    dbb = DatabaseBuilder()
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 9090
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    # Start a thread with the server -- that thread will then start one
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    while True:
        pass
    server.shutdown()