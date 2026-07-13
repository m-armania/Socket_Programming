#!/usr/bin/env python3
from socket import *
servername='192.168.50.238'
serverport=12000
clientsocket=socket(AF_INET,SOCK_STREAM)
clientsocket.connect((servername,serverport))
while True:
	message=input('Enter a message in lowercase:\n')
	if message == 'quit':
		break
	clientsocket.send(message.encode())
	modifiedmessage=clientsocket.recv(2048)
	print ('From server:',modifiedmessage.decode())
clientsocket.close()

