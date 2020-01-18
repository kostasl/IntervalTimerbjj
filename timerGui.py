#!/usr/bin/python
import RPi.GPIO as GPIO

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
global lblEasterEgg

iRounds = 0 ##Count the number of rounds passed
troundTime = 0.3 ##min
trestTime = 0.21

##Using Pin Names
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Button to GPIO21


def showEasterEgg():
	global lblEasterEgg 
	#lblRound.pack_forget()
	if (not lblEasterEgg.winfo_ismapped() ):
		lblEasterEgg.pack()
		lblEasterEgg.place(relx=0.2, rely=0.15, anchor=CENTER)

def hideEasterEgg():
	global lblEasterEgg
	lblEasterEgg.pack(side="bottom")
	lblEasterEgg.pack_forget() ##Hide it

def showRound(iRounds):
	lblRound.pack()
	lblRound.place(relx=0.8, rely=0.1, anchor=CENTER)
	txtRound.set('Round {:2}'.format(iRounds) )

def formatTimerString(remainder):
	return( '{:02}:{:02}'.format(int(remainder.total_seconds()/60), int(remainder.total_seconds())) )

def quit(*args):
    root.destroy()
    
def show_Resttime(endTime): 
	global iRounds
	##Set State Aesthetics
	root.configure(background='blue')
	lbl.config(background="blue",foreground="black")
    # Get the time remaining until the event
	remainder = endTime - datetime.now()
    
	##play Time Approach beep
	#if (remainder.total_seconds()  10 ):
		
	if (remainder.total_seconds() <= 10 ):
		sndBeep.play()
		showEasterEgg()
	
	# remove the microseconds part
	#remainder = remainder - timedelta(microseconds=remainder.microseconds)
    # Show the time left on  the global label object
	txt.set(formatTimerString(remainder))

	if (remainder.total_seconds() > 1):
		# Trigger the countdown after 1000ms
		root.after(1000, show_Resttime,endTime)
	else:
		sndCombat.play()
		endTime = datetime.now() + timedelta(minutes=troundTime)
		iRounds = iRounds + 1 ##Increment Number of Rounds
		#txtRound.set('Round {:2}'.format(iRounds) )
		showRound(iRounds)
		root.after(1000, show_Roundtime,endTime)


def show_Roundtime(endTime):
	##Set State Aesthetics
	root.configure(background='black')
	lbl.config(background="black",foreground="#81ced4")
	hideEasterEgg()
	

	# Get the time remaining until the event
	remainder = endTime - datetime.now() + timedelta(seconds=1)

    # remove the microseconds part
	remainder = remainder - timedelta(microseconds=remainder.microseconds)

	##play Time Approach beep
	if (remainder.total_seconds() <= 10 ):
		sndBeep.play()

	# Show the time left on  the global label object
	txt.set(formatTimerString(remainder))
	
	#print(remainder.total_seconds())

	if (remainder.total_seconds() > 1):
		# Trigger the countdown after 1000ms
		root.after(1000, show_Roundtime,endTime)

	else:
		# Set the end date and time for the countdown
		endTime = datetime.now() + timedelta(minutes=trestTime)
		sndParrol.play()
		root.after(1000, show_Resttime,endTime)


pygame.init()
## Load Resources 
sndBeep = pygame.mixer.Sound("res/beep.wav")
sndParrol = pygame.mixer.Sound("res/parol.wav")
sndCombat = pygame.mixer.Sound("res/combats.wav")


# Use tkinter lib for showing the clock
root = Tk()
root.attributes("-fullscreen", True)
root.bind("x", quit)

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
imgEasterEgg  = ImageTk.PhotoImage(Image.open("res/mattbatten.jpeg") )
#ImageTk.resize((450, 332), Image.ANTIALIAS) 
imglogo = ImageTk.PhotoImage(Image.open("res/neonLogo.jpeg") )


##Aesthetics 
fnt = font.Font(family='Verdana', size=80, weight='bold')
txt = StringVar()
lbl = ttk.Label(root, textvariable=txt, font=fnt, foreground="#81ced4", background="black")
lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

txtRound = StringVar()
lblRound = ttk.Label(root, textvariable=txtRound, font=fnt, foreground="#81ced4", background="black")

##Add Logo To Center top
lbllogo = ttk.Label(root, image=imglogo).pack(side="top")

lblEasterEgg = ttk.Label(root, image=imgEasterEgg) ##.pack(side="top")
lblEasterEgg.pack_forget() ##Hide it
##Start The Round Timer recursive 
iRounds = iRounds + 1

surface = pygame.Surface((800,600))
pygame.draw.circle(surface,pygame.Color(250, 250, 250,200),(300, 60), 50, 10)

# Set the end date and time for the countdown
endTime = datetime.now() + timedelta(minutes=troundTime,seconds=1)
showRound(iRounds)
show_Roundtime(endTime)
#root.after(0, show_Roundtime,)

try:
    while True:
         button_state = GPIO.input(21)
         if button_state == False:
         	 showEasterEgg()
             print('Button Pressed...')
             time.sleep(0.2)
         else:
             hideEasterEgg()
except:
    GPIO.cleanup()


root.mainloop()
