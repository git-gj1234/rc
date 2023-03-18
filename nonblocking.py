import socket
import time
import errno

listener_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ''
PORT = 5005
server_endpoint = (server_address, PORT)
listener_socket.bind(server_endpoint)

listener_socket.setblocking(False)
# set to non-blocking

while True:

  try:

    max_data_size = 1000
    payload, client_endpoint = listener_socket.recvfrom(max_data_size)

  except socket.error as e:
    if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
        # no data available for reading

      print('no data available for reading')
      time.sleep(1)
      continue

  data = payload.decode()
  print(data, 'received from', client_endpoint)
