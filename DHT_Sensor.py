import time
import board
import adafruit_dht

# Initial the dht device, with data pin connected to:
<<<<<<< HEAD
##GPIO pin 4 (Pin N 7)
dhtDevice = adafruit_dht.DHT22(board.D4)

while True:
    try:
#        dhtDevice = adafruit_dht.DHT22(board.D4)
=======
dhtDevice = adafruit_dht.DHT22(board.D7)

while True:
    try:
>>>>>>> e8caa60224879da76ff149a09bef1f9d1edd1867
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% "
              .format(temperature_f, temperature_c, humidity))

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])

<<<<<<< HEAD
    time.sleep(2.0)
=======
    time.sleep(2.0)
>>>>>>> e8caa60224879da76ff149a09bef1f9d1edd1867
