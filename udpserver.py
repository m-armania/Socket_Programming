from socket import *
serverPort = 12000
serversocket = socket(AF_INET,SOCK_DGRAM)
serversocket.bind(('', serverPort))
print("The server is ready to receive")
while True:
    message, addr = serversocket.recvfrom(2048)
    modifiedmessage = message.decode().count('a')  # Count occurrences of the letter 'a'
    serversocket.sendto(str(modifiedmessage).encode(), addr)