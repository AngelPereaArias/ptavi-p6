#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Clase (y programa principal) para un servidor de eco en UDP simple. """

import socketserver
import os
import sys


class EHand(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        methods = ["ACK", "BYE", "INVITE"]

        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            line = line.decode("utf-8")
            method = line[:line.find(" ")]
            if len(line) >= 2:
                if method == "INVITE":
                    Msg = b"SIP/2.0 100 Trying\r\n\r\n"
                    Msg += b"SIP/2.0 180 Ring\r\n\r\n"
                    Msg += b"SIP/2.0 200 OK\r\n\r\n"
                    self.wfile.write(Msg)

                elif method == "ACK":
                    IP = sys.argv[1]
                    os.system("./mp32rtp -i " + IP + " -p 23032 < " + song)

                elif method == "BYE":
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

                elif method and method not in methods:
                    print(method)
                    self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")

                else:
                    self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

            print("-Cliente: " + line)


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        serv = socketserver.UDPServer((sys.argv[1], int(sys.argv[2])), EHand)
        song = sys.argv[3]
    except:
        sys.exit("Usage: python3 server.py.py IP Port cancion.mp3")

    print("Lanzando servidor UDP de eco...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
