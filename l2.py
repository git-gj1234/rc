# Import all files from
# tkinter and overwrite
# all the tkinter files
# by tkinter.ttk
from tkinter import *
from tkinter.ttk import *

# function to be called when
# keyboard buttons are pressed
def key_press(event):
	
	print(event.keycode, 'is pressed')

# creates tkinter window or root window
root = Tk()
root.geometry('200x100')
root.bind('<Key>', key_press)

# here we are binding keyboard
# with the main window
while True:
	
	root.update()

