import socket
import time
# Library underlying all networking related activity

listener_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# -> Socket to receive data
# -> All network communications happen through sockets after all

server_address = '192.168.1.2'
# '' or '0.0.0.0' implies all network adapters in the computer
PORT = 5005
# -> Other clients must use this PORT to interact with this application
# -> No other application can be running with the same PORT in this computer

server_endpoint = (server_address, PORT)
# Our network endpoint that other computers can connect to

listener_socket.bind(server_endpoint)
# Connecting our socket to the network endpoint

while True:
  # forever active server
  
  max_data_size = 1000
  # we specify a maximum on the receive buffer to prevent bufferoverflows
  # (larger data must be split across multiple packets)

  payload, client_endpoint = listener_socket.recvfrom(max_data_size)
  # -> recvfrom pauses until data is sent to listener_socket
  # -> if received packet is larger than max_data_size, it is rejected (with an error)
  # -> payload: binary data received
  # -> client_endpoint: sender of the data

  data = payload.decode()
  # convert from binary back to original data

  print(data, 'received from', client_endpoint)
