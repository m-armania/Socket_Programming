from socket import *
serverport=12000
serversocket=socket(AF_INET,SOCK_STREAM)
serversocket.bind(('',serverport))
serversocket.listen(1)
print('The server is ready to recieve')
while True:
    connectionsocket,addr=serversocket.accept()
    print('connected to:',addr)
    while True:
        message=connectionsocket.recv(2048)
        if not message:
            break
        decoded=message.decode() # Count occurrences of the letter 'a'
        modifiedmessage=decoded.count('a') + decoded.count('A') 
        connectionsocket.send(str(modifiedmessage).encode())
    connectionsocket.close()