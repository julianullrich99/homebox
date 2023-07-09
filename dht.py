import RPi.GPIO as GPIO
import adafruit_dht

class dhtSense():
    def __init__(self,config={}):
        self.config = config

        print(config)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        
        try:
          self.sensor = adafruit_dht.DHT11(self.config['pin'])
        except Exception as e:
          print(e)

        self.lastTemp = 1.0
        self.lastHum = 1.0

    def read(self):
      try:
        self.lastTemp = self.sensor.temperature
        self.lastHum = self.sensor.humidity
      except Exception as e:
        # print(e)
        pass
      
      # print(self.lastTemp)

      return {
          'temp': self.lastTemp,
          'hum': self.lastHum
      }