import curses


import socket
import sys


class Client():

    def __init__(self, host, port, stdscr):
        self.host, self.port = host, port
        self.stdscr = stdscr

    def run(self):
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server
            sock.connect((self.host, self.port))
            while True:
                ch = self.stdscr.getch()
                if ch == curses.ERR:
                    continue

                if ch == ord('a'):
                    # Send data
                    sock.sendall(bytes("a" + "\n", "utf-8"))
                    # Receive data from the server and shut down
                    received = str(sock.recv(1024), "utf-8")
                    self.stdscr.addstr(0, 1, received)

                if ch == ord('q'):
                    break
        finally:
            sock.close()


def main(stdscr):
    stdscr.nodelay(1)
    curses.noecho()
    curses.cbreak()
    curses.endwin()
    curses.curs_set(False)
    stdscr.keypad(True)

    c = Client("localhost", 9999, stdscr)
    c.run()


if __name__ == '__main__':
    curses.wrapper(main)