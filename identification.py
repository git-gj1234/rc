import socket
import time
import errno
import threading

IDENTIFICATION_PORT = 5005
# clients broadcast to this port to identify users on the network

class Controller_token:
  def __init__(self):
    self.is_active = False
  def enable(self):
    self.is_active = True
  def disable(self):
    self.is_active = False
# for controlling identification

# identification thread's job
def _start_identification(username, identification_controller):
  identification_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  server_address = ''
  identification_endpoint = (server_address, IDENTIFICATION_PORT)
  identification_socket.bind(identification_endpoint)

  identification_socket.setblocking(False)

  while True:

    while not identification_controller.is_active:
      time.sleep(0.1)

    try:
      max_data_size = 1000
      payload, client_endpoint = identification_socket.recvfrom(max_data_size)

    except socket.error as e:
      if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
        time.sleep(0.1)
        continue

    command = payload.decode()
    if command == 'identify':
        # they are querying our username
      encoded_username = username.encode()
      identification_socket.sendto(encoded_username, client_endpoint)
      # we send our username


############## EXPORTED FUNCTIONS ##############

def set_username(username):
  global _identification_controller
  _identification_controller = Controller_token()
  _identification_thread = threading.Thread(target=_start_identification, args=(username, _identification_controller,))
  _identification_thread.start()

def go_online():
  if not _identification_controller:
    raise RuntimeError('no username set')
  _identification_controller.enable()

def go_offline():
  if not _identification_controller:
    raise RuntimeError('no username set')
  _identification_controller.disable()
