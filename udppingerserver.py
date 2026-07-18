import random   # We will need the following module to generate randomized lost packets
from socket import *    # Create a UDP socket  
serverSocket = socket(AF_INET, SOCK_DGRAM)  # Notice the use of SOCK_DGRAM for UDP packets
serverSocket.bind(('', 12000))   # Assign IP address and port number to socket 
while True: 
    rand = random.randint(0, 10)    # Generate random number in the range of 0 to 10      
    message, addr = serverSocket.recvfrom(1024)  # Receive the client packet along with the address it is coming from
    modifiedmessage = message.upper()   # Capitalize the message from the client 
    if rand < 4:    # If rand is less is than 4, we consider the packet lost and do not respond 
        continue 
    serverSocket.sendto(modifiedmessage, addr)   # Otherwise, the server responds    