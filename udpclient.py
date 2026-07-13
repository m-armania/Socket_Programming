#!/usr/bin/env python3
from socket import *
servername = '192.168.50.238'
serverport = 12000
clientsocket = socket(AF_INET,SOCK_DGRAM)
while True:
	message = input("input lowercase sentence:")
	if message.lower()== 'quit':
		break
	clientsocket.sendto(message.encode(),(servername,serverport))
	modifiedmessage,serveraddress = clientsocket.recvfrom(2048)
	print (modifiedmessage.decode())
clientsocket.close()
