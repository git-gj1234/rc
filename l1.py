import socket
from tkinter import *
import tkinter as tk
import time
import random

GAME_PORT = 5007
global isFailed
global score1
global score2
# represents the game state
board = ''
def moveBaseLR(base, direction, x, y = 0):
    x1, y1, x2, y2 = c.coords(base)
    if ((x1 > 0 and direction == 'l') or (x2 < 400 and direction == 'r')):
        c.move(base, x, y)
        c.update()

def startBall(ball, speed):
    global score1
    global score2
    s = random.randint(-speed, speed)
    x, y = s,speed #Start. Ball to move in random direction. 0-speed is used to get negative value
    c.move(ball, x, y)

    for p in range(1, 500000):
        l, t, r, b = c.coords(ball)
        txtS.delete(0, END)
        #txtS2.delete(0, END)
        txtS.insert(0, str(score1))
        #txtS2.insert(0, str("score2"))
        #Need to change direction on hitting wall. Eight options are there.
        if(r >= 400 and x >= 0 and y < 0): #Ball moving ↗ and hit right wall
            x, y = 0-speed, 0-speed
        elif(r >= 400 and x >= 0 and y >= 0): #Ball moving ↘ and hit right wall
            x, y = 0-speed, speed
        elif(l <= 0 and x < 0 and y < 0): #Ball moving ↖ and hit left wall
            x, y = speed, 0-speed
        elif(l <= 0 and x < 0 and y >= 0): #Ball moving ↙ and hit left wall
            x, y = speed, speed
        # elif(t <= 0 and x >= 0 and y < 0): #Ball moving ↗ and hit top wall
        #     x, y = speed, speed
        # elif(t <= 0 and x < 0 and y < 0): #Ball moving ↖ and hit top wall
        #     x, y = 0-speed, speed
        elif(b >= 385): #Ball reached base level. Check if base touches ball
            tchPt = l + 10 #Size is 20. Half of it.
            bsl, bst, bsr, bsb = c.coords(base)
            if(tchPt >= bsl and tchPt <= bsr): #Ball touch base
                n = random.randint(-speed, speed)
                x, y = n, 0-speed
            else: #Hit bottom. Failed
                c.itemconfigure(lblID, state='normal')
                global isFailed
                isFailed = True
                score1 = score1+1
                print(score1,score2)
                txtS.delete(0, END)
                #txtS2.delete(0, END)
                txtS.insert(0, str(score1))
                #txtS2.insert(0, str(score2))
                break

        elif(b <= 40): #Ball reached base level. Check if base touches ball
            tchPt = l + 10 #Size is 20. Half of it.
            bsl, bst, bsr, bsb = c.coords(base2)
            if(tchPt >= bsl and tchPt <= bsr): #Ball touch base
                n = random.randint(-speed, speed)
                x, y =  0-speed,speed
            else: #Hit bottom. Failed
                c.itemconfigure(lblID, state='normal')
                score2 = score2+1
                print(score1,score2)
                isFailed = True
                
                txtS2.delete(0, END)
                
                txtS2.insert(0, str(score2))
                break
        
        time.sleep(.025)
        c.move(ball, x, y)
        c.update()
    
def restart():
    global isFailed
    if(isFailed == True):
        isFailed = False
        c.itemconfigure(lblID, state='hidden')
        c.moveto(base, 150, 385)
        c.moveto(ball, 190, 365)
        startBall(ball, ballspeed)


  
def key_press(event):
  pressed_key = (event.keycode)
  if(pressed_key == 37):
      moveBaseLR(base, 'l', 0-basespeed)
      game_socket.send(pressed_key.encode())
  if(pressed_key == 38):
      moveBaseLR(base2, 'l', 0-basespeed)
      game_socket.send(pressed_key.encode())
  if(pressed_key == 39):
      moveBaseLR(base, 'r', basespeed)
      game_socket.send(pressed_key.encode())
  if(pressed_key == 40):
      moveBaseLR(base2, 'r', basespeed)
      game_socket.send(pressed_key.encode())
  
def get_move(pressed_key):
  if(pressed_key == 37):
      moveBaseLR(base, 'l', 0-basespeed)
  if(pressed_key == 38):
      moveBaseLR(base2, 'l', 0-basespeed)
  if(pressed_key == 39):
      moveBaseLR(base, 'r', basespeed)
  if(pressed_key == 40):
      moveBaseLR(base2, 'r', basespeed)
 

def game_server():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as accepter_socket:
      accepter_socket.bind(('', GAME_PORT))
      accepter_socket.listen(1)

      game_socket, addr = accepter_socket.accept()

      with game_socket:
        print('Game Started')
      global root,score1,score2,basespeed,ball,ballspeed,isFailed,base,base2,txtScore,txtScore2,txtS2,txtS,c,lblID
      root = Tk()
    
      score1 = 0
      score2 = 0
      root.minsize(400,400)
      basespeed = 10
      ballspeed = 5
      
      isFailed = False

      c = Canvas(width=400, height=400, background='#000')
      coordinates = 0,200,400,200

  # Draw a dashed vertical line, 5px dash and 1px space
      c.create_line(coordinates, dash=(5,1), fill="white")
      c.pack()
      base = c.create_rectangle(150, 385, 250, 400, fill='blue', outline='blue')
      base2 =  c.create_rectangle(150, 0, 250, 20, fill='blue', outline='blue')
      ball = c.create_oval(190, 365, 210, 385, fill='red', outline='red')    
      txtS = tk.Entry(c, text='2')
      txtS2 = tk.Entry(c, text='1')
      txtScore = c.create_window(380, 180, anchor='nw', window=txtS)
      txtScore2 = c.create_window(380, 200, anchor='nw', window=txtS2)
      

      lblM = tk.Label(c, text='Failed!!!Press Enter key to start again')
      lblID = c.create_window(100, 190, anchor='nw', window=lblM)
      c.itemconfigure(lblID, state='hidden')
        
      while True:

        root.update()
        root.bind('<Key>',key_press)    
        print(game_socket.recv(1024).decode())    
        p_key = game_socket.recv(1024).decode()
        get_move(p_key)

def game_client(opponent):
  global game_socket
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as game_socket:
      game_socket.connect((opponent, GAME_PORT))
      print('Game Started')

      global root,score1,score2,basespeed,ball,ballspeed,isFailed,base,base2,txtScore,txtScore2,txtS2,txtS,c,lblID
      root = Tk()
    
      score1 = 0
      score2 = 0
      root.minsize(400,400)
      basespeed = 10
      ballspeed = 5
      
      isFailed = False

      c = Canvas(width=400, height=400, background='#000')
      coordinates = 0,200,400,200

  # Draw a dashed vertical line, 5px dash and 1px space
      c.create_line(coordinates, dash=(5,1), fill="white")
      c.pack()
      base = c.create_rectangle(150, 385, 250, 400, fill='blue', outline='blue')
      base2 =  c.create_rectangle(150, 0, 250, 20, fill='blue', outline='blue')
      ball = c.create_oval(190, 365, 210, 385, fill='red', outline='red')    
      txtS = tk.Entry(c, text='2')
      txtS2 = tk.Entry(c, text='1')
      txtScore = c.create_window(380, 180, anchor='nw', window=txtS)
      txtScore2 = c.create_window(380, 200, anchor='nw', window=txtS2)
      

      lblM = tk.Label(c, text='Failed!!!Press Enter key to start again')
      lblID = c.create_window(100, 190, anchor='nw', window=lblM)
      c.itemconfigure(lblID, state='hidden')

      while True:

        root.update()
        root.bind('<Key>',key_press)        
        p_key = game_socket.recv(1024).decode()
        get_move(p_key)
        





import socket

GAME_PORT = 5007

# represents the game state
board = ''

def print_current_board():
  print('board:..')

def get_users_move():
  move = input('What is your move: ')
  return move

def update_game_state(player, move):
  global board 
  # update the board
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

      with game_socket:
        print('Game Started')
        
        while True:

          print("waiting for opp's move")
          opp_move = game_socket.recv(1024).decode()
          if not opp_move:
            break
          update_game_state('opp', opp_move)
          if has_game_ended():
            break

          print_current_board()
          move = get_users_move()
          update_game_state('user', move)
          game_socket.send(move.encode())
          if has_game_ended():
            break

      print_current_board()
      print('Game ended')

def game_client(opponent):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as game_socket:
      game_socket.connect((opponent, GAME_PORT))
      print('Game Started')

      while True:

        print_current_board()
        move = get_users_move()
        update_game_state('user', move)
        game_socket.send(move.encode())
        if has_game_ended():
          break

        print("waiting for opp's move")
        opp_move = game_socket.recv(1024).decode()
        if not opp_move:
          break
        update_game_state('opp', opp_move)
        if has_game_ended():
          break

  print_current_board()
  print('Game ended')















  def key_press(event):
  pressed_key = (event.keycode)
  if(pressed_key == 37):
      moveBaseLR(base, 'l', 0-basespeed)
      game_socket.send(str(pressed_key).encode())
  if(pressed_key == 38):
      moveBaseLR(base2, 'l', 0-basespeed)
      game_socket.send(str(pressed_key).encode())
  if(pressed_key == 39):
      moveBaseLR(base, 'r', basespeed)
      game_socket.send(str(pressed_key).encode())
  if(pressed_key == 40):
      moveBaseLR(base2, 'r', basespeed)
      game_socket.send(str(pressed_key).encode())
  
def get_move(pressed_key):
  if(pressed_key == '37'):
      moveBaseLR(base, 'l', 0-basespeed)
  if(pressed_key == '38'):
      moveBaseLR(base2, 'l', 0-basespeed)
  if(pressed_key == '39'):
      moveBaseLR(base, 'r', basespeed)
  if(pressed_key == '40'):
      moveBaseLR(base2, 'r', basespeed)





# __________________________________


import socket
from tkinter import *
from tkinter.ttk import *

GAME_PORT = 5007

# represents the game state
board = ''
def key_press(event):
	
	print(event.keycode, 'is pressed')
def print_current_board():
  print('board:..')

def get_users_move():
  move = input('What is your move: ')
  return move

def update_game_state(player, move):
  global board 
  # update the board
  if(move != 'g'):
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

      with game_socket:
        print('Game Started')
        
        #print("waiting for opp's move")
        #opp_move = game_socket.recv(1024).decode()
      
        #update_game_state('opp', opp_move)
        root2 = Tk()
        root2.geometry('200x100')
        root2.bind('<Key>', key_press)
        while True:

          root2.update()
          #print_current_board()
          #move = get_users_move()
          #update_game_state('user', move)
          accepter_socket.listen(1)
          move = 'g'
          game_socket, addr = accepter_socket.accept()
          game_socket.send(move.encode())
          



def game_client(opponent):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as game_socket:
      game_socket.connect((opponent, GAME_PORT))
      print('Game Started')
      root = Tk()
      root.geometry('200x100')
      root.bind('<Key>', key_press)
      while True:

        root.update()
        move = 'g'
        #game_socket.send(move.encode())
        

        
        #opp_move = game_socket.recv(1024).decode()
        #if not opp_move:
        #  break
        




