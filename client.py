# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import socket

try:
    import pickle
except ImportError:
    import cPickle as pickle

# TEST: --user pl, --pass lp --host localhost --port 9090

class Client():
    def __init__(self, args):
        self.is_connected = False
        self.user, self.password, self.host, self.port = args
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self._send_credentials()
        self._remove_password()

    def _send_credentials(self):
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
            print(response)
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

    def where_am_I(self, user):
        """
        Determine in which zone the user is.  Response from server is Picklified
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