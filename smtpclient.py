#!/usr/bin/env python3
from socket import *
msg = "\r\n I love you."
end msg = "\r\n.\r\n"
mailserver = google mail server
clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect(mailserver)
recv = clientsocket.recv(1024).decode()
print (recv)
if recv[:3] != '220':
	print ('220 reply not received from the server.')
helocommand = 'HELO Diana\r\n'



