#!/usr/bin/python

import pygame

from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import ImageTk, Image ##For Jpeg

from datetime import datetime,timedelta,time


global endTime 
global iRounds ##Number of Roll Rounds 
global troundTime ##Duration of each round
global trestTime ##Duration of each round

iRounds = 5
troundTime = 1 ##min
trestTime = 1



def quit(*args):
    root.destroy()
    
def show_Resttime(endTime): 
	root.configure(background='blue')
    # Get the time remaining until the event
	remainder = endTime - datetime.now()
    # remove the microseconds part
	remainder = remainder - timedelta(microseconds=remainder.microseconds)
    # Show the time left on  the global label object
	txt.set(remainder)

	if (remainder.total_seconds() > 1):
		# Trigger the countdown after 1000ms
		root.after(1000, show_Resttime,endTime)
	else:
		root.after(1000, show_Roundtime,endTime)

def show_Roundtime(endTime):
	root.configure(background='black')
	# Get the time remaining until the event
	remainder = endTime - datetime.now()
    # remove the microseconds part
	remainder = remainder - timedelta(microseconds=remainder.microseconds)
	# Show the time left on  the global label object
	txt.set(remainder)
	print(remainder.total_seconds())
	if (remainder.total_seconds() > 1):
		# Trigger the countdown after 1000ms
		root.after(1000, show_Roundtime,endTime)
	else:
		# Set the end date and time for the countdown
		endTime = datetime.now() + timedelta(minutes=trestTime)
		root.after(1000, show_Resttime,endTime)

# Use tkinter lib for showing the clock
root = Tk()
root.attributes("-fullscreen", True)

root.bind("x", quit)

# Set the end date and time for the countdown
endTime = datetime.now() + timedelta(minutes=troundTime)

##Aesthetics 
fnt = font.Font(family='Helvetica', size=60, weight='bold')
txt = StringVar()
lbl = ttk.Label(root, textvariable=txt, font=fnt, foreground="green", background="black")
lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
imglogo = ImageTk.PhotoImage(Image.open("res/neonLogo.jpeg") )
lbllogo = ttk.Label(root, image=imglogo).pack(side="top")

##Start The Round Timer recursive 
root.after(1000, show_Roundtime,endTime)

root.mainloop()
