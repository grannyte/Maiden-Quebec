# -*- coding: utf-8 -*-
from __future__ import print_function

import sys

import argparse
import re
import socket

"""
    Game client using threads to manage connections.  Server is using the TCP protocol and
    might not suit game over Internet.  It is best to host local network games.  As this game
    is a prototype, you are urged to not push it to his limit; keep the number of connections low.
"""

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
            if response == expect:
                print(response)
                self.is_connected = True
        except Exception:
            print("An error occured while sending credentials", file=sys.stderr)
            raise
        assert self.is_connected, "User must not be connected to the server"

    def _remove_password(self):
        """
        Delete the password for security purpose.  Currently, there is no security whatsoever
        :return:
        """
        self.password = None
        del self.password

    def quit(self):
        self.sock.close()


def parser_args():
    parser = argparse.ArgumentParser(prog="maid", description="MaindenQuebec's client")
    parser.add_argument('--user', type=str, required=True, help="Player's user name")
    parser.add_argument('--password', type=str, required=True, help="Player's password")
    parser.add_argument('--host', type=str, required=True, help="Server's hostname")
    parser.add_argument('--port', type=int, required=True, help="Server's listening port")
    args =  parser.parse_args()
    # TODO: Add others regex
    if len(re.match(r'\w{1,16}', args.user).group(0)) != len(args.user):
        raise Exception("User name must have between 1 and 16 (inclusive) character from A to Z, a to z, 0 to 9 and _")
    return args.user, args.password, args.host, args.port


if __name__ == '__main__':
    args = parser_args()
    client = Client(args)
    client.quit()
