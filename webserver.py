from threading import Thread
from socket import *                     #In order to terminate the program
serverport = 6789
serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serversocket.bind(('',serverport))
serversocket.listen(5)
def handle_client(connectionsocket, addr):
        print(f'Connected to {addr}')
        try:
            message = connectionsocket.recv(2048).decode()  #Receive the request message from the client
            print(f'Received message:\n{message}')
            filename=message.split()[1]
            f=open(filename[1:])
            outputdata=f.read()
            connectionsocket.send('HTTP/1.1 200 OK\r\n Content-Type: text/html\r\n\r\n'.encode())  #These are the header lines which indicate that the request was successful
            for i in range(0, len(outputdata)):
                connectionsocket.send(outputdata[i].encode())   #Send the content of the requested file to the client
            connectionsocket.send("\r\n".encode())              #Indicates that the connection is closed
        except (IOError, IndexError, ValueError) as e:
            print(f'Error handling {addr}: {e}')
            outputdata = "<html><head></head><body><h1>404 Not Found</h1></body></html>"
            connectionsocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
        finally:
            connectionsocket.close()
print('Ready to serve...')
while True:
    connectionsocket, addr = serversocket.accept()
    client_thread = Thread(target=handle_client, args=(connectionsocket, addr))
    client_thread.start()