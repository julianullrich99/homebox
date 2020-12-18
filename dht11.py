import RPi.GPIO as GPIO
import Python_DHT as dht

class dhtSense():
    def __init__(self,config={}):
        self.config = config

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        # self.sensor = dht.DHT11(pin = config['pin'])
        self.sensor = dht.DHT11
        self.pin = config['pin']

    def read(self):
        hum, temp = dht.read_retry(self.sensor, self.pin)

        return {
            'temp': temp,
            'hum': hum
        }