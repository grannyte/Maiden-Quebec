# -*- coding: utf-8 -*-

import argparse
import src.serveur as serveur
import socketserver


def main():
    """
    Point d'entré du programme.  Celui-ci valide que les arguments passés en paramètre
    sont conformes.
    """

    parser = argparse.ArgumentParser(description='Text-based game')
    parser.add_argument('-i', '--irrlicht',
                        help='Irrlicht manages graphics(Not implemented yet)',
                        action='store_true')
    parser.parse_args()


def run_server():
    """Démarre le serveur"""
    host, port = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((host, port), serveur.Server)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

if __name__ == "__main__":
    main()
    run_server()
