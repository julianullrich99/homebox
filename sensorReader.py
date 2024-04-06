import threading
import time

import dht
import externalMQTT
import average

class sensorReader(threading.Thread):
    def __init__(self,config = {}, name=""):
        threading.Thread.__init__(self, name=name)

        self.targetTemp = 18
        self.currentTemp = 1
        self.heating = 0
        self.checkInterval = 5 # checkintervall in sekunden (auch fürs logging)
        self.active = False

        averageValues = 5
        self.averageTemp = average.average(averageValues)
        self.averageHum = average.average(averageValues)

        self.switch = externalMQTT.externalMQTT({
            'defaultTopic': config['switchTopic'],
            'client': config['mqttClient']
        })

        self.metrics = externalMQTT.externalMQTT({
            'defaultTopic': config['metricTopic'],
            'client': config['mqttClient']
        })

        self.heaterActiveMqtt = externalMQTT.externalMQTT({
            'defaultTopic': config['heaterActiveTopic'],
            'client': config['mqttClient']
        })

        self.sensor = dht.dhtSense({
            'pin': config['sensorPin']
        })

    def run(self):
        while True:
            data = self.sensor.read()

            self.currentTemp = self.averageTemp.get(data['temp'])
            # hum = self.averageHum.get(data['hum'])

            self.metrics.send(data['temp'])

            if (self.active):
              if (self.targetTemp > self.currentTemp):
                  self.switch.send(1)
                  self.heating = 1
              else:
                  self.switch.send(0)
                  self.heating = 0
            else:
              self.switch.send(0)

            time.sleep(self.checkInterval)

    def setMQTT(self,value):
        # sets the desired Temperature
        self.targetTemp = float(value)
        self.setActive('1')
        self.heaterActiveMqtt.send('1')

    def setActive(self, value):
      self.active = value == '1'
      print("Active {}".format(self.active))

    def setScheduler(self,value):
        self.targetTemp = float(value)
    
