# -*- coding: utf-8 -*-
from __future__ import print_function

"""
    Game Server using threads to manage connections.  Server is using the TCP protocol and
    might not suit game over Internet.  It is best to host local network games.  As this game
    is a prototype, you are urged to not push it to his limit; keep the number of connections low.
"""

import sys
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
        try:
            if request.startswith('LOGIN'):
                response = self.request_login(request)
            elif request.startswith('LOGOUT'):
                response = self.request_logout(request)
            elif request.startswith('WHERE'):
                response = self.request_logout(request)
            else:
                response = self.request_anything_else(request)
        except Exception as e:
            print_function(e, file=sys.stderr)
            raise
        piclify = pickle.dumps(response)
        print(response)
        print(piclify)
        self.request.sendall(piclify)

    def request_login(self, request):
        _, user, password = request.split(' ')
        date_in = datetime.datetime.now(datetime.timezone.utc).timestamp()
        self.db.login(user, date_in)
        msg = '{} {}'.format(user, 'has been successfully connected.', 'ascii')
        return {'answer': 'OK', 'msg': msg}

    def request_logout(self, request):
        _, user = request.split(' ')
        date_out = datetime.datetime.now(datetime.timezone.utc).timestamp()
        self.db.logout(user, date_out)
        msg = '{} {}'.format(user, 'has been successfully disconnected.', 'ascii')
        return {'answer': 'OK', 'msg': msg}

    def where_am_I(self, request):
        _, user = request.split(' ')
        zone = self.db.where_am_I(user)
        return {'answer': 'OK', 'user': user, 'zone': zone}

    def request_anything_else(self, request):
        raise NotImplementedError('Someone made an unusual request')


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