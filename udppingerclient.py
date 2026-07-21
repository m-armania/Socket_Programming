#!/usr/bin/env python3
import time
from socket import *
servername = '192.168.50.238'
serverport = 12000
clientsocket = socket(AF_INET, SOCK_DGRAM)
clientsocket.settimeout(1.0)
sent = 0
received = 0
rtts = []
for seq in range(1, 11):
	tim = time.ctime()
	message = f'Ping {seq} {tim}'
	sent += 1
	try:
		start = time.time()
		clientsocket.sendto(message.encode(), (servername, serverport))
		modifiedmessage, addr = clientsocket.recvfrom(2048)
		elapsedtime = time.time() - start
		received += 1
		rtts.append(elapsedtime)
		print (f'From server: {modifiedmessage.decode()}, rtt = {elapsedtime: .4f}s')
	except timeout:
		print (f'{seq}: Request timed out!')
clientsocket.close()
loss = (sent - received) / sent * 100
print (f'\n--- {servername} ping statistics---')
print (f'{sent} packets transmitted, {received} packets received, {loss}% packets lost')
if rtts:
	mn = min(rtts)
	mx = max(rtts)
	avg = sum(rtts) / len(rtts)
	mdev = (sum((x - avg)**2 for x in rtts) / len(rtts))**0.5
	print (f'rtt min/max/avg/mdev = {mn:.4f}/{mx:.4f}/{avg:.4f}/{mdev:.4f}s')
