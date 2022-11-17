import RPi.GPIO as GPIO
import adafruit_dht

class dhtSense():
    def __init__(self,config={}):
        self.config = config

        print(config)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        
        self.sensor = adafruit_dht.DHT11(self.config['pin'])

        self.lastTemp = 1
        self.lastHum = 1

    def read(self):
      try:
        self.lastTemp = self.sensor.temperature
        self.lastHum = self.sensor.humidity
      except:
        # print("could not read dht11 sensor")
        pass
      
      # print(self.lastTemp)

      return {
          'temp': self.lastTemp,
          'hum': self.lastHum
      }