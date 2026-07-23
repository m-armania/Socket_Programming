#!usr/bin/env python3
import sys
from socket import *
servername = sys.argv[1]
serverport = int(sys.argv[2])
filename = sys.argv[3]
clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect((servername, serverport))
message = f'GET {filename} HTTP/1.1\r\nHost:{servername}\r\nConnection: keep alive\r\n\r\n\r\n'
clientsocket.send(message.encode())
while True:
	response = clientsocket.recv(4096)
	if len(response) < 1:
		break
	print ('From server:\r\n',response.decode())
clientsocket.close()
