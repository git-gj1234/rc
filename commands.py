import socket
# Library underlying all networking related activity

hostname = socket.gethostname()
# -> Every device identifies itself in its local network by hostname
# -> Will be unique in the local network

ip_address = socket.gethostbyname( hostname )
# -> All network communication happens between IP addresses (and ports)
# -> Every network adapter is identified uniquely by an IP address
# -> gethostbyname resolves hostname to one IP address (may be multiple)

interfaces = socket.getaddrinfo(host=hostname, port=None)
# -> For getting all ip addresses under a hostname
# -> For IPv4, add family=socket.AF_INET

broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# -> Creates a UDP socket
# -> All network communication happen through sockets

broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# -> Enables broadcasting for the socket
# -> To prevent unintentional broadcasts

broadcast_address = '192.168.1.2'
# IPv4 address reserved for broadcasting

PORT = 5005
# -> Computers have multiple network applications
#    PORT identifies which application you want to interact with

network_endpoint = (broadcast_address, PORT)
# The network endpoint we want to interact with

data = 'Hello World!'
# can't be sent over the network

encoded_data = data.encode()
# can be sent over the network - binary data

broadcast_socket.sendto(encoded_data, network_endpoint)
# Sends encoded_data to network_endpoint according to broadcast_socket's protocol
