# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import re
import socket

"""
    Game client using threads to manage connections.  Server is using the TCP protocol and
    might not suit game over Internet.  It is best to host local network games.  As this game
    is a prototype, you are urged to not push it to his limit; keep the number of connections low.
"""

class Client():
    def __init__(self, args):
        self.user, self.password, self.host, self.port = args
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.is_connected = False
        print(self.socket.recv(1024))  # print welcome message
        #self.socket.setblocking(0)  # Asynchronous BlockingIOError: [Errno 11] Resource temporarily unavailable

    def _format_msg(self, msg):
        return bytes(msg, "ascii")

    def send_credentials(self):
        """
        Send credentials as plain text
        :return:
        """
        assert not self.is_connected, "User must not be connected to the server"
        credential = self._format_msg('CONNECTING ' + self.user + ' ' + self.password)
        expect = self.user + ' has been successfully connected.'
        while not self.is_connected:
            try:
                self.socket.send(credential)
                data = self.socket.recv(512).decode("ascii")
                if data == expect:
                    self.is_connected = True
            except socket.timeout:
                """no data yet"""
        print(expect)
        # Get rid of password as it won't be use anymore
        self.password = None
        del self.password
        assert self.is_connected, "User must be connected to the server"

    def run(self):
        assert self.is_connected, "User must be connected to the server"
        while self.is_connected:
            try:
                # send up user input and receive back server' permission, event and updates
                data = socket.recv(512)
            except socket.error:
                '''no data yet..'''

    def quit(self):
        self.socket.close()

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
    client.send_credentials()
    client.quit()
