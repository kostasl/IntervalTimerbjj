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
<code>
sudo apt-get update  
sudo apt-get install python3-pip    
</code>

Install virtual environment, cd into IntervalTimerbjj:  
<code> 
python3 -m pip install --user virtualenv  
python3 -m venv env  
source env/bin/activate  
</code>

ImageTK  and pygame:   
<code>
pip3 install pygame  
sudo apt-get install python3-pil.imagetk  
pip3 install Pillow  
</code>

library for GPIO access to input buttons:  
<code>
pip3 install RPi.GPIO
</code>

Adafruit library for temperature and humidity sensor (Either Option):
Deprecated version that still works:
<code>
sudo pip3 install Adafruit_DHT
</code>
Manual Installation:  
<code>
git clone https://github.com/adafruit/Adafruit_Python_DHT.git  
cd Adafruit_Python_DHT  
sudo apt-get update  
sudo apt-get install build-essential python-dev  
sudo python3 setup.py install  
</code>
The above library works, but needs our timer python script to be run as sudo:   
<code>
sudo python3 timerGui.py
<\code> 

More recent version, with which I had trouble using:
(Still within our virtual environment):    
<code>
pip3 install adafruit-circuitpython-dht
sudo apt-get install libgpiod2
<\code>
this one seems to work only for user pi.
In any case add user to the gpio group:
groupadd <user> gpio


##Oss!
### Konstantinos Lagogiannis 2020



