#!/usr/bin/env python3
import ssl
import os
from socket import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
sender = 'abcd@gmail.com'
receiver = 'efgh@yahoo.com'
message = MIMEMultipart()
message['From'] = sender
message['To'] = receiver
message['Subject'] = 'Text and image'
message.attach(MIMEText('I love u.\r\n', 'plain'))
image_path = os.path.expanduser('~/Downloads/images.jpeg')
with open(image_path, 'rb') as f:
	img_data = f.read()
image = MIMEImage(img_data, name = os.path.basename(image_path))
message.attach(image)
msg = message.as_string()
endmsg = ".\r\n"
mailserver = 'smtp.gmail.com'
clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect((mailserver, 587))
recv = clientsocket.recv(1024).decode()
print (recv)
if recv[:3] != '220':
	print ('220 reply not received from the server.')
clientsocket.send(b'EHLO Guess\r\n')
recv1 = clientsocket.recv(1024).decode()
print (recv1)
if recv1[:3] != '250':
        print ('250 reply not received from the server')
clientsocket.send(b'STARTTLS\r\n')
print (clientsocket.recv(1024).decode())
context = ssl.create_default_context()
clientsocket = context.wrap_socket(clientsocket, server_hostname = mailserver)
clientsocket.send(b'EHLO Dian\r\n')
recv2 = clientsocket.recv(1024).decode()
print (recv2)
if recv2[:3] != '250':
	print ('250 reply not received from the server')
clientsocket.send(b'MAIL FROM: <abcd@gmail.com>\r\n')
recv3 = clientsocket.recv(1024).decode()
print (recv3)
if recv3[:3] != '250':
	print ('250 reply not received from the server')
clientsocket.send(b'RCPT TO: <mdarmaan99@gmail.com>\r\n')
recv4 = clientsocket.recv(1024).decode()
print (recv4)
if recv4[:3] != '250':
	print ('250 reply not received from the server')
clientsocket.send(b'DATA\r\n')
recv5 = clientsocket.recv(1024).decode()
print (recv5)
if recv5[:3] != '354':
	print ('354 reply not received from the server')
msgdata = msg + endmsg
clientsocket.send(msgdata.encode())
recv6 = clientsocket.recv(1024).decode()
print (recv6)
if recv6[:3] != '250':
	print('250 reply not received from the server')
clientsocket.send(b'QUIT\r\n')
recv7 = clientsocket.recv(1024).decode()
print (recv7)
if recv7[:3] != '221':
	print ('221 reply not received from the server')
clientsocket.close()

