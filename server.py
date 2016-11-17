#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import os
import sys

os.system("clear")

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        methods = ["ACK", "BYE", "INVITE"]
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion\r\n")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            line = line.decode("utf-8")
            method = line[:line.find(" ")]
            
            if method == "INVITE":
                Msg = b"SIP/2.0 100 Trying\r\n\r\n"
                Msg += b"SIP/2.0 180 Ring\r\n\r\n"
                Msg += b"SIP/2.0 200 OK\r\n\r\n"
                self.wfile.write(Msg)
                
            elif method == "ACK":
                
                os.system("./mp32rtp -i " + sys.argv[1] + " -p 23032 < " + sys.argv[3])
            elif method == "BYE":
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                
            elif method not in methods:
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")

            else:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

            print("-Cliente: " + line)


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((sys.argv[1], int(sys.argv[2])), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
