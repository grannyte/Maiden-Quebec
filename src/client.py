# -*- coding: utf-8 -*-

import socket
import sys


class Client():

    def __init__(self, host, port):
        self.host, self.port = host, port

    def run(self):
        data = " ".join(sys.argv[1:])

        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect((self.host, self.port))
            sock.sendall(bytes(data + "\n", "utf-8"))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-8")
        finally:
            sock.close()

        print("Sent:     {}".format(data))
        print("Received: {}".format(received))


def run_client():
    c = Client("localhost", 9999)
    c.run()

if __name__ == "__main__":
    run_client()
