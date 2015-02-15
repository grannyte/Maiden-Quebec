# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import socket

"""
    Game client using threads to manage connections.  Server is using the TCP protocol and
    might not suit game over Internet.  It is best to host local network games.  As this game
    is a prototype, you are urged to not push it to his limit; keep the number of connections low.
"""

# TEST: --user pl, --pass lp --host localhost --port 9090

class Client():
    """
    Singleton that represents the client connections
    """
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
        :return:
        """
        assert not self.is_connected, "User must not be connected to the server"
        credentials = bytes("CONNECTING {} {}".format(self.user, self.password), 'ascii')
        expect = self.user + ' has been successfully connected.'
        try:
            self.sock.sendall(credentials)
            response = str(self.sock.recv(1024), 'ascii')
            print(response)
            if response == expect:
                self.is_connected = True
            else:
                raise Exception("Cannot connect to server")
        except Exception:
            print("An error occurred while sending credentials", file=sys.stderr)
            raise
        assert self.is_connected, "User must be connected to the server"

    def _remove_password(self):
        """
        Delete the password for security purpose.  Currently, there is no security whatsoever
        :return:
        """
        self.password = None
        del self.password

    def request_entities(self, zone):
        """
        Ask the server for all entities in the map
        :return:
        """
        assert zone is not None
        request = bytes("ENTITIES {}".format(zone), 'ascii')
        try:
            self.sock.sendall(request)
            response = str(self.sock.recv(1024), 'ascii')
        except Exception:
            print("An error occurred while asking for zone entities", file=sys.stderr)
            raise




    def quit(self):
        self.sock.close()