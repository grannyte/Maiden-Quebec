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

try:
    import pickle
except ImportError:
    import cPickle as pickle


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.db = Database()  # TODO: close database   with:  keyword
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        """
        Receives plain text (predetermined request from client)
        sends pickled dict (wide variety of answers)
        BEWARE: pickle is not safe
        :return:
        """
        request = str(self.request.recv(1024), 'ascii').strip()
        if request.startswith('LOGIN'):
            response = self.request_login(request)
        elif request.startswith('LOGOUT'):
            response = self.request_logout(request)
        elif request.startswith('ZONE'):
            _, zone = request.split(' ')
        elif request.startswith('ENTITIES'):
            pass
        else:
            response = self.request_anything_else(request)
        self.request.sendall(pickle.dump(response))

    #TODO: replace if else with try catch instead
    def request_login(self, request):
        _, user, password = request.split(' ')
        if self.db.is_user_connected(user):
            return bytes("{} {}".format(user, 'is already connected.'), 'ascii')
        else:
            date_in = datetime.datetime.now(datetime.timezone.utc).timestamp()
            self.db.login(user, date_in)
            return bytes("{} {}".format(user, 'has been successfully connected.'), 'ascii')

    def request_logout(self, request):
        _, user = request.split(' ')
        if self.db.is_user_connected(user):
            date_out = datetime.datetime.now(datetime.timezone.utc).timestamp()
            self.db.logout(user, date_out)
            return bytes("{} {}".format(user, 'has been successfully disconnected.'), 'ascii')
        else:
            return bytes("{}".format('Are you messing with the server ?'), 'ascii')

    def request_zone(self, request):
        _, zone = request.split(' ')
        if self.db.does_zone_exist(zone):
            pass
        else:
            # TODO: generate map via L-System and send it back.  The player is sending false packets
            pass

    def request_anything_else(self, request):
        print('Someone made an unusual request')
        return {".": None}

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