# -*- coding: utf-8 -*-

import socketserver


class Server(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


def run_server():
    """Démarre le serveur"""
    host, port = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((host, port), Server)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

if __name__ == "__main__":
    run_server()
