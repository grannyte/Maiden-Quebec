# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import socket

try:
    import pickle
except ImportError:
    import cPickle as pickle

#
# TEST: --user pl, --pass lp --host localhost --port 9090

class Client():
    def __init__(self, args):
        self.is_connected = False
        self.user, self.password, self.host, self.port = args
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self._login()
        self._remove_password()

    def _login(self):
        """
        Send credentials as plain text, synchronous transmission
        :return: {'answer': 'OK', 'msg': msg}
        """
        assert not self.is_connected, "User must not be already connected to the server"
        try:
            credentials = bytes("LOGIN {} {}".format(self.user, self.password), 'ascii')
            self.sock.sendall(credentials)
            response = self.sock.recv(1024)
            print(response)
            response = pickle.loads(response)
            if response['answer'] != 'OK':
                raise Exception('An error occurred while sending credentials')
        except:
            raise
        self.is_connected = True
        assert self.is_connected, "User must be connected to the server"

    def _remove_password(self):
        """
        Delete the password for security purpose.  Currently, there is no security whatsoever
        :return:
        """
        self.password = None
        del self.password

    def who_is(self, user):
        """
        Looks what is the player made of
        :param user: the player's name.
            Here, user and player are the same even though a user might might/should have multiple players
        :return:
        """
        try:
            request = bytes("USER {}".format(self.user), 'ascii')
            self.sock.sendall(request)
            response = self.sock.recv(1024)
            response = pickle.loads(response)
            if response['answer'] != 'OK':
                raise Exception('An error occurred while searching user in database')
            response.pop('answer', None)
            return response
        except:
            raise


    def where_is(self, user):
        """
        Determine in which zone the user is.
        :param user: The user which the zone is required
        :return: {'answer': 'OK', 'user': user, 'zone': zone}
        """
        try:
            request = bytes("WHERE {}".format(user), 'ascii')
            self.sock.sendall(request)
            response = self.sock.recv(1024)
            if response['answer'] != 'OK':
                raise Exception('An error occurred while asking user zone')
            return response.zone
        except:
            raise

    def quit(self):
        self.sock.close()