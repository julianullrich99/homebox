import threading
import time

import dht
import externalMQTT
import average

class heaterControl(threading.Thread):
    def __init__(self,config = {}, name=""):
        threading.Thread.__init__(self, name=name)

        self.targetTemp = 18
        self.currentTemp = 1
        self.heating = 0
        self.checkInterval = 5 # checkintervall in sekunden (auch fürs logging)
        self.active = False
        self.config = config
        self.metricTopic = config['metricTopic']

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
            try:
                data = self.sensor.read()

                if data['temp'] == 1 and data['hum'] == 1:
                        continue 


                self.currentTemp = self.averageTemp.get(data['temp'])

                self.metrics.send(data['temp'], f"{self.metricTopic}/temp")
                self.metrics.send(data['hum'], f"{self.metricTopic}/hum")

                if (self.active):
                  if (self.targetTemp > self.currentTemp):
                      self.switch.send(1)
                      self.heating = 1
                  else:
                      self.switch.send(0)
                      self.heating = 0
                else:
                  self.switch.send(0)

            except:
                pass
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
    
