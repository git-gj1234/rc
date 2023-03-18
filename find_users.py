import socket
import time
import errno

IDENTIFICATION_PORT = 5005


############## EXPORTED FUNCTIONS ##############

def find_online_users():

  users_query_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  users_query_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  users_query_socket.setblocking(False)
  broadcast_address = '255.255.255.255'
  identification_endpoint = (broadcast_address, IDENTIFICATION_PORT)

  command = 'identify'
    # later we can add more commands like get_user_statistics
  encoded_command = command.encode()

  users_query_socket.sendto(encoded_command, identification_endpoint)
  waiting_time = 1 # seconds to wait for responses
  time.sleep(waiting_time) # wait 

  users = []
  # read all responses
  while True:
    try:
      max_data_size = 1000
      payload, client_endpoint = users_query_socket.recvfrom(max_data_size)
      username = payload.decode()
      ip_address = client_endpoint[0]

      # add user to list
      user = {'username': username, 'ip_address': ip_address}
      users.append(user)

    except socket.error as e:
      if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
          # all respones have been read
        break
  
  return users
