import socket
from tkinter import *
from tkinter.ttk import *
import time
import errno
GAME_PORT = 5007

def key_press(event,game_socket):
  #print("a\n"*10)
  a = str(event.keycode)
  print(a)
  game_socket.send(a.encode())
  #print("sent")

  
# represents the game state
board = ''

#def print_current_board():
#  print('board:..')

#def get_users_move():
#  move = input('What is your move: ')
#  return move

def update_game_state(player, move):
  global board 

  if(move ):
    if(( move.lstrip('g'))):
      if(move.lstrip('g').rstrip('g')):
       print(move.lstrip('g').rstrip('g'))
  # update the board
  
  if 'g' not in move:
    board = board + move
    print(player + ' played ' + move)

def has_game_ended():
  if (board == 'abcd'):
    return True
  else:
    return False

def game_server():

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as accepter_socket:
      accepter_socket.bind(('', GAME_PORT))
      accepter_socket.listen(1)

      game_socket, addr = accepter_socket.accept()
      game_socket.setblocking(False)

      with game_socket:
        print('Game Started')

        root2 = Tk()
        root2.geometry('200x100')
       
        root2.bind('<Key>', lambda event: key_press(event,game_socket),game_socket)
        
        while True:

          root2.update()
          try :
            opp_move = game_socket.recv(1024)
          except socket.error as e:
            if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
              continue
          
          # if not opp_move:
          #   break
          opp_move = opp_move.decode()
          update_game_state('opp', opp_move)


      #print_current_board()
      print('Game ended')

def game_client(opponent):

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as game_socket:
      game_socket.connect((opponent, GAME_PORT))
      game_socket.setblocking(False)
      print('Game Started')

      root2 = Tk()
      root2.geometry('200x100')
      root2.bind('<Key>', lambda event: key_press(event,game_socket),game_socket)

      while True:


        
        root2.update()
        #print_current_board()
        
        try :
          opp_move = game_socket.recv(1024)
        except socket.error as e:
          if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
            continue
        
        # if not opp_move:
        #   break
        opp_move = opp_move.decode()
        update_game_state('opp', opp_move)
        
        
        if has_game_ended():
          break
        time.sleep(0.25)

  #print_current_board()
  print('Game ended')