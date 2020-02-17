# IntervalTimerbjj
In an attempt to contribute to the martial arts gym opened by my friends here in Southampton, UK, I made this simple interval timer that we can use for time keeping the roll rounds in Brazilian Jiu-Jitsu.

It is designed to run on a Raspberry Pi Zero connected to a display with sound. 
To avoid the need to use a mouse and keyboard or touchscreen,  the timer reads input from a  button connected  (through pull_up) to GPIO pin 21. 
The  main idea was to keep this simple so anyone can use who is running the class. In this spirit this is  timer has a single button that is used to start and stop/reset.
With the addition of a AM2302 Sensor connected to GPIO pin 4, the timer also displays the room's temperature and humidity.   
 
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

Adafruit library for temperature and humidity sensor (Either Option).  
You can try with the deprecated version that still works:    
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
</code> 

More recent version, which runs without need for sudo :
(Still within our virtual environment):    
<code>
pip3 install adafruit-circuitpython-dht  
sudo apt-get install libgpiod2  
</code>  
If you hit permission problems then add user to the gpio group:  
<code>
groupadd \<user\> gpio  
</code>
If still in trouble then try running with user pi.

## Adding Run on startup
(courtesy of [https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/all])  
Method : autostart
If you need access to elements from the X Window System (e.g. you are making a graphical dashboard or game), then you will need to wait for the X server to finish initializing before running your code. One way to accomplish this is to use the autostart system.
### create .Desktop file
<code>
mkdir /home/pi/.config/autostart  
nano /home/pi/.config/autostart/timer.desktop    
</code>
Copy in the following text into the timer.desktop file:    
<code> 

[Desktop Entry]      
Type=Application    
Name=Neon Timer  
Exec=bash -c 'cd /home/pi/workspace/IntervalTimerbjj/ && source env/bin/activate && /usr/bin/python3 timerGui.py'    
Path=home/pi/workspace/IntervalTimerbjj/   
GenericName=A timer for Bjj rounds down at Neon Martial Arts  
Comment[en_US]=Start the Full Screen Timer  
</code>
 
#Internet Connection
Check  /etc/network/interfaces.
 
Routing table:  
<code>
sudo route -n  
</code>

DHCP Request:  
<code>
sudo dhclient -v eth0
</code>
Add Gateway in case it is missing:
<code>
sudo route add default gw 192.168.0.1 enx00ea4c680036
</code>

xset dpms reports missing extension:
<code>
sudo apt install libxcb-dpms0
<\code>
##Oss!
### Konstantinos Lagogiannis 2020



