#!/usr/bin/env python3
import time
from socket import *
servername = '192.168.50.238'
serverport = 12000
clientsocket = socket(AF_INET, SOCK_DGRAM)
clientsocket.settimeout(1.0)
for seq in range(10):
	message = 'hello os'
	try:
		start = time.time() 
		clientsocket.sendto(message.encode(), (servername, serverport))
		modifiedmessage, addr = clientsocket.recvfrom(2048)
		elapsedtime = time.time() - start
		print (f'{modifiedmessage.decode()}, time = {elapsedtime: .4f}s')
	except timeout:
		print (f'{seq}: Request timed out!')
clientsocket.close()

	
