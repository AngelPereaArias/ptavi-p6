#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente que abre un socket a un servidor."""

import socket
import sys
import os

# Cliente UDP simple.
os.system("clear")

try:
    METHOD = sys.argv[1]
    Aux = sys.argv[2]
    Aux_Line = Aux[:Aux.find(":")]
    RECEIVER = Aux[:Aux.find("@")]
    IP = Aux[Aux.find("@")+1:Aux.rfind(":")]
    PORT = int(Aux[Aux.rfind(":")+1:])

except:
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")

# Contenido que vamos a enviar
if METHOD == ("INVITE"):
    LINE = "INVITE " + Aux_Line + " SIP/2.0"
elif METHOD == ("ACK"):
    LINE = "ACK " + Aux_Line + " SIP/2.0"
elif METHOD == ("BYE"):
    LINE = "BYE " + Aux_Line + " SIP/2.0"

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PORT))

print("Enviando: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
