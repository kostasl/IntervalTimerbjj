#!/usr/bin/python

RPI_PLATFORM = True
PIN_BUTTONA = 21
PIN_BUTTONB = 16

if RPI_PLATFORM:
	try:
		import RPi.GPIO as GPIO
	except ImportError:
		print("Not running on a Raspberry pi")
		RPI_PLATFORM = False

import pygame

from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import ImageTk, Image ##For Jpeg

import colorsys as colsys

from datetime import datetime,timedelta,time


global endTime 
global iRounds ##Number of Roll Rounds 
global troundTime ##Duration of each round
global trestTime ##Duration of each round
global sndParrol,sndCombat
global lblEasterEgg
global cState ##Timer State

iRounds = 0 ##Count the number of rounds passed
troundTime = 5 ##min
trestTime = 1
AFTER_ROUNDTMR = None

from enum import Enum
class TimerState(Enum):
		STOPPED = 1
		ROLL = 2
		REST = 3

class ButtonState(Enum):
		BUTTONPRESSED = False
		BUTTONRELEASED = True
#		BUTTONCOMMAND


cState = TimerState(1)
bStateA = ButtonState(True)
bStateB = ButtonState(True) ##The Change Interval Button

##Using Pin Names
if RPI_PLATFORM:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Button to GPIO21
	bStateA = ButtonState(GPIO.input(21))
	bStateB = ButtonState(GPIO.input(16))

# convert colour from integer tuple to Hex Value string
def _from_rgb(rgb):
    #"""translates an rgb tuple of int to a tkinter friendly color code
    #"""
    return "#%02x%02x%02x" % rgb


def changeInterval(*args):
	global troundTime
	stopTimer()
	sndBeep.play()
	print("Change Interval");

	if (troundTime == 5):
		troundTime = 3
	else:
		troundTime = 5

	print("Change Interval to %(interval)d min" % {"interval":troundTime} );
	resetTimer()

	

def quit(*args):
	root.destroy()

def resetTimer():
	global cState,AFTER_ROUNDTMR
	root.after_cancel(AFTER_ROUNDTMR) ##Empty the call timer Queue

	cState = TimerState.STOPPED
	endTime = datetime.now() + timedelta(minutes=troundTime, seconds=0)
	show_Roundtime(endTime)


def stopTimer():
	global cState,AFTER_ROUNDTMR
	cState = TimerState.STOPPED
	root.after_cancel(AFTER_ROUNDTMR)

	showEasterEgg()
	print('STOP STATE')

# Restarts Round
def startTimer():
	global cState
	cState = TimerState.ROLL
	endTime = datetime.now() + timedelta(minutes=troundTime, seconds=0)
	showRound(iRounds)  ##Start The Timer
	show_Roundtime(endTime)
	print('ROLL STATE')
	hideEasterEgg()
	sndCombat.play()


# Keyboard Input / Toggle Time State
def InputToggle(args):
	global cState
	print("Key Pressed")
	if (cState == TimerState.STOPPED):
		startTimer()
	elif (cState == TimerState.ROLL or cState == TimerState.REST):
		stopTimer()


##Does Button Debounce Through Delay Read
def checkPushButton():
	global cState
	global bStateA,bStateB
	button_stateA = not bStateA
	button_stateB = not bStateB
	if RPI_PLATFORM:
		button_stateA = GPIO.input(21) #Button A for Start/pause
		button_stateB = GPIO.input(16) #Button B for Sw Interval

	##Check If Button Changed State - Now Pressed
	if (button_stateA == False and (bStateA == ButtonState.BUTTONRELEASED) ):
		bStateA = ButtonState.BUTTONPRESSED
		print('Button A Pressed.')
		## If Timer Was Stopped Then Button Should Start it 
		if (cState == TimerState.STOPPED):
			startTimer()
		else:
			stopTimer()
	## Set Button Released
	elif (button_stateA == True and (bStateA == ButtonState.BUTTONPRESSED)):
		bStateA = ButtonState.BUTTONRELEASED
		print('Button A Released.')

	##Check If Button B Changed State
	if (button_stateB == False and (bStateB == ButtonState.BUTTONRELEASED) ):
		bStateB = ButtonState.BUTTONPRESSED
		print('Button B Pressed.')
		changeInterval()
	elif (button_stateB == True and (bStateB == ButtonState.BUTTONPRESSED)):
		bStateB = ButtonState.BUTTONRELEASED
		print('Button B Released.')
	
	# Delay Recursive
	root.after(100, checkPushButton)


def showEasterEgg():
	global lblEasterEgg 
	#lblRound.pack_forget()
	if (not lblEasterEgg.winfo_ismapped() ):
		lblEasterEgg.pack()
		lblEasterEgg.place(relx=0.13, rely=0.72, anchor=CENTER)

def hideEasterEgg():
	global lblEasterEgg
	lblEasterEgg.pack(side="bottom")
	lblEasterEgg.pack_forget() ##Hide it

def showRound(iRounds):
	lblRound.pack()
	lblRound.place(relx=0.5, rely=0.7, anchor=CENTER)
	txtRound.set('Round {:2}'.format(iRounds) )

def formatTimerString(remainder):
	minutes, seconds = divmod(remainder.total_seconds(), 60)
	return( '{:02}:{:02}'.format(int(minutes  ), int(seconds) ) )

def bgColourChange(col):
	root.configure(background=_from_rgb(col))
	lbl.config(background=_from_rgb (col),foreground="black")
	lblRound.config(background=_from_rgb (col),foreground="black")

# Recursive Call to go up down the blue Colours to show rest breathing effect
def bgColourAnimate(i,dir):
	##Animate BG Colour - Show Breathing Rythm
	t = 0
	#for col in (col_blue):
	#root.after( (200*len(col_blue) + 200*(t-len(col_blue) )  ), bgColourChange, col)
	t += 1
	##iF sTILL in REST sTATE tHEN REPEAT Colour Cycle
	#if (cState == TimerState.REST):

	##Ladder Up/Down The idx
	if (i == (len(col_blue)-1) ):
		dir=-1 ##Down
	elif (i == 0):
		dir=1 ##Up Again

	#print(i)
	bgColourChange( col_blue[i])
	i=dir+i
	if (cState == TimerState.REST):
		root.after(150, bgColourAnimate, i,dir)


def show_Resttime(endTime):
	global iRounds,cState

	#	pygame.time.delay(200)
	if (cState == TimerState.STOPPED):
		return(0)

	# Get the time remaining until the event
	remainder = endTime - datetime.now()

	##play Time Approach beep
	if (remainder.total_seconds() <= 10 and remainder.total_seconds() > 1 ):
		sndBeep.play()
		#showEasterEgg()
    
    # remove the microseconds part
    #remainder = remainder - timedelta(microseconds=remainder.microseconds)
# Show the time left on  the global label object
	txt.set(formatTimerString(remainder))

	if (remainder.total_seconds() > 1):
			# Carry Rest CountDown If Timer Is not Stopped
			if (cState != TimerState.STOPPED):
				root.after(1000, show_Resttime,endTime)
	else:
			sndCombat.play()
			endTime = datetime.now() + timedelta(minutes=troundTime)
			iRounds = iRounds + 1 ##Increment Number of Rounds
            #txtRound.set('Round {:2}'.format(iRounds) )
			showRound(iRounds)
			hideEasterEgg()
			if (cState != TimerState.STOPPED):
				cState = TimerState.ROLL
				root.after(1000, show_Roundtime,endTime)


def show_Roundtime(endTime):
	global cState,AFTER_ROUNDTMR
	##Set State Aesthetics / Black BG
	root.configure(background='black')
	lbl.config(background="black",foreground="#81ced4")
	lblRound.config(background="black",foreground="#81ced4")

	remainder = timedelta(minutes=troundTime)
	##If this was queued while time reset - then do not update the display 
	if (cState != TimerState.STOPPED):
		# Get the time remaining until the event
		remainder = endTime - datetime.now() + timedelta(seconds=1)


    # remove the microseconds part
	#remainder = remainder - timedelta(microseconds=remainder.microseconds)

	##play Time Approach beep
	if (remainder.total_seconds() <= 10 and remainder.total_seconds() > 1  ):
		sndBeep.play()

	# Show the time left on  the global label object
	txt.set(formatTimerString(remainder))
	
	#print(remainder.total_seconds())

	if (remainder.total_seconds() > 1 ): #and (cState == TimerState.ROLL)
		# Carry Rest CountDown If Timer Is not Stopped
		if (cState != TimerState.STOPPED):
			# Trigger the countdown after 1000ms
			AFTER_ROUNDTMR = root.after(1000, show_Roundtime,endTime)

	else:
		# Set the end date and time for the countdown
		endTime = datetime.now() + timedelta(minutes=trestTime)
		sndParrol.play()
		cState = TimerState.REST # Change Time Stater To REST
		
		root.after(1000, show_Resttime,endTime)
		root.after(1000, bgColourAnimate,0,1)

pygame.init()
## Load Resources
## This pygame mixer method produces an unreliable output in Rasp Zero / vlc has been suggested as alternative
pygame.mixer.init()
sndBeep = pygame.mixer.Sound("res/beep.wav")
sndParrol = pygame.mixer.Sound("res/parol.wav")
sndCombat = pygame.mixer.Sound("res/combats.wav")


# Use tkinter lib for showing the clock
root = Tk()
root.attributes("-fullscreen", True)
root.bind("q", quit)
root.bind("t", changeInterval)

root.bind("<space>", InputToggle)


#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
imgEasterEgg  = ImageTk.PhotoImage(Image.open("res/mattbatten.jpeg") )
#ImageTk.resize((450, 332), Image.ANTIALIAS) 
imglogo = ImageTk.PhotoImage(Image.open("res/neonLogo.jpeg") )


##Aesthetics 
fnt = font.Font(family='Verdana', size=80, weight='bold')
fnts = font.Font(family='Verdana', size=60, weight='bold')
txt = StringVar()
lbl = ttk.Label(root, textvariable=txt, font=fnt, foreground="#81ced4", background="black")
lbl.place(relx=0.5, rely=0.5, anchor=CENTER)
#hsv_to_rgb(h, s, v)    Convert the color from HSV coordinates to RGB coordinates.

## Make Array of Colours For The Breathing/Rest Animation
i=0
col_blue = []
while  (i < 21):
	col_blue.append( tuple(round(i * 255) for i in colsys.hsv_to_rgb(209/360,0.4 + 0.6*i/21,1) ) )
	#print( col_blue[i] )
	i += 1

txtRound = StringVar()
lblRound = ttk.Label(root, textvariable=txtRound, font=fnts, foreground="#81ced4" , background="black")

##Add Logo To Center top
lbllogo = ttk.Label(root, image=imglogo).pack(side="top")

lblEasterEgg = ttk.Label(root, image=imgEasterEgg) ##.pack(side="top")
lblEasterEgg.pack_forget() ##Hide it
##Start The Round Timer recursive 
iRounds = iRounds + 1

surface = pygame.Surface((800,600))
#pygame.Color(250, 250, 250,200)
pygame.draw.circle(surface,col_blue[1],(300, 60), 50, 10)

#root.after(0, show_Roundtime,)

root.after(10, checkPushButton)

    
root.mainloop()
if (RPI_PLATFORM):
	GPIO.cleanup()