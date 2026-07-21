import random   # We will need the following module to generate randomized lost packets
import time     # We will need the following module to measure the round trip time
from socket import *  # Create a UDP socket  
serverSocket = socket(AF_INET, SOCK_DGRAM)  # Notice the use of SOCK_DGRAM for UDP packets
serverSocket.bind(('', 12000))   # Assign IP address and port number to socket
HEARTBEAT_TIMEOUT = 1  # Set the heartbeat timeout to 1 second
lost = 0  # Initialize the lost packet count
while True: 
    start = time.time()   # Start the timer to measure the round trip time
    rand = random.randint(0, 10)    # Generate random number in the range of 0 to 10      
    message, addr = serverSocket.recvfrom(1024)  # Receive the client packet along with the address it is coming from
    print ("\r\nReceived message: ", message.decode())  # Print the received message
    modifiedmessage = message.upper()   # Capitalize the message from the client 
    if rand < 4:    # If rand is less is than 4, we consider the packet lost and do not respond
        print (f"Packet lost (random number: {rand})")   # Increment the lost packet count 
        lost += 1
        continue 
    serverSocket.sendto(modifiedmessage, addr)   # Otherwise, the server responds
    rtt = time.time() - start   # Calculate the round trip time
    print (f"Round trip time: {rtt:.3f} seconds , Lost packets: {lost}")   # Print the round trip time and the number of lost packets