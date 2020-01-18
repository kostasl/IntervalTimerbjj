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
global sndParrol,sndCombat

iRounds = 0 ##Count the number of rounds passed
troundTime = 1 ##min
trestTime = 0.5



def quit(*args):
    root.destroy()
    
def show_Resttime(endTime): 
	##Set State Aesthetics
	root.configure(background='blue')
	lbl.config(background="blue",foreground="black")
    # Get the time remaining until the event
	remainder = endTime - datetime.now()
    # remove the microseconds part
	remainder = remainder - timedelta(microseconds=remainder.microseconds)
    # Show the time left on  the global label object
	txt.set(formatTimerString(remainder))

	if (remainder.total_seconds() > 1):
		# Trigger the countdown after 1000ms
		root.after(1000, show_Resttime,endTime)
	else:
		sndCombat.play()
		endTime = datetime.now() + timedelta(minutes=troundTime)
		root.after(1000, show_Roundtime,endTime)

def formatTimerString(remainder):
	return( '{:02}:{:02}'.format(int(remainder.total_seconds()/60), int(remainder.total_seconds())) )

def show_Roundtime(endTime):
	##Set State Aesthetics
	root.configure(background='black')
	lbl.config(background="black",foreground="#81ced4")

	# Get the time remaining until the event
	remainder = endTime - datetime.now()
    # remove the microseconds part
	remainder = remainder - timedelta(microseconds=remainder.microseconds)
	# Show the time left on  the global label object
	txt.set(formatTimerString(remainder))
	print(remainder.total_seconds())
	if (remainder.total_seconds() > 1):
		# Trigger the countdown after 1000ms
		root.after(1000, show_Roundtime,endTime)
	else:
		# Set the end date and time for the countdown
		endTime = datetime.now() + timedelta(minutes=trestTime)
		sndParrol.play()
		root.after(1000, show_Resttime,endTime)


pygame.init()
sndParrol = pygame.mixer.Sound("res/parol.wav")
sndCombat = pygame.mixer.Sound("res/combats.wav")


# Use tkinter lib for showing the clock
root = Tk()
root.attributes("-fullscreen", True)

root.bind("x", quit)

# Set the end date and time for the countdown
endTime = datetime.now() + timedelta(minutes=troundTime)

##Aesthetics 
fnt = font.Font(family='Verdana', size=80, weight='bold')
txt = StringVar()
lbl = ttk.Label(root, textvariable=txt, font=fnt, foreground="#81ced4", background="black")
lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
imglogo = ImageTk.PhotoImage(Image.open("res/neonLogo.jpeg") )
lbllogo = ttk.Label(root, image=imglogo).pack(side="top")

##Start The Round Timer recursive 
root.after(0, show_Roundtime,endTime)

root.mainloop()
