# IntervalTimerbjj
In an attempt to contribute to the martial arts gym opened by my friends here in Southampton, UK, I made this simple interval timer that we can use for time keeping the roll rounds in Brazilian Jiu-Jitsu.

It is designed to run on a Raspberry Pi Zero connected to a display with sound. 
To avoid the need to use a mouse and keyboard or touchscreen,  the timer reads input from a  button connected  (through pull_up) to GPIO pin 21. 
The  main idea was to keep this simple so anyone can use who is running the class. In this spirit this is  timer has a single button that is used to start and stop/reset.
 
The timer has two countdown states, going from active (fight round) countdown, and then to a rest period countdown before the next round
countdown initiates. It keeps track of the number of cycles/Rounds and displays it on the main interface. It makes a warning beeps during the last 10sec before countdown in either state is due.
     

This version has been customized my for my gym, Neon Martial Arts, showing its logo through the playback of voices for Parol (End the fight)
and "Combats".
 It also allows of cheeky hidden (easteregg) picture of one of your training buddies to appear when its time to select a new partnet.

I am new to python and thus this little fun project has helped me get more acquainted with this scripting language.  
I used tkinter for interface design, and pygame for sound playback.

##Issues:
 Pygame  appears to not be very reliable on the pi Zero and sounds breakup or do not synchronize.

## Installation :
*sudo apt-get update
*sudo apt-get install python3-pip
* pip3 install Pygame
* Adafruit library (Either Option):
    * (Deprecated) sudo pip install Adafruit_DHT
This one can be run by sudo from any user   
Or:
    * (Newer) pip3 install adafruit-circuitpython-dht
    * sudo apt-get install libgpiod2
this one seems to work only for user pi.
In any case add user to the gpio group:
groupadd <user> gpio
 

##Oss!
### Konstantinos Lagogiannis 2020



