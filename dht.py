import RPi.GPIO as GPIO
import dht11

class dhtSense():
    def __init__(self,config={}):
        self.config = config

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        self.sensor = dht11.DHT11(pin = config['pin'])

        # self.sensor = dht.DHT11
        # self.pin = config['pin']

    def read(self):
        data = self.sensor.read()
        # print(data.temperature)
        # print(data.humidity)
        # print(data.is_valid())

        return {
            'temp': data.temperature,
            'hum': data.humidity
        }