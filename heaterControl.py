import threading
import time

import dht11
import externalMQTT
import average

class heaterControl(threading.Thread):
    def __init__(self,config = {}, name=""):
        threading.Thread.__init__(self, name=name)

        self.targetTemp = 0
        self.currentTemp = 1
        self.heating = 0
        self.checkInterval = 5 # checkintervall in sekunden (auch fürs logging)

        averageValues = 5
        self.averageTemp = average.average(averageValues)
        self.averageHum = average.average(averageValues)

        self.switch = externalMQTT.externalMQTT(config['mqttClient'], {
            'defaultTopic': config['switchTopic']
        })

        self.metrics = externalMQTT.externalMQTT(config['mqttClient'], {
            'defaultTopic': config['metricTopic']
        })

        self.sensor = dht11.dhtSense({
            'pin': config['sensorPin']
        })

    def run(self):
        while True:
            data = self.sensor.read()

            self.currentTemp = self.averageTemp.get(data['temp'])
            hum = self.averageHum.get(data['hum'])

            self.metrics.send(self.currentTemp)

            if (self.targetTemp > self.currentTemp):
                self.switch.send(1)
                self.heating = 1
            else:
                self.switch.send(0)
                self.heating = 0

            time.sleep(self.checkInterval)

    def setMQTT(self,value):
        # sets the desired Temperature
        self.targetTemp = float(value)

    def setScheduler(self,value):
        self.targetTemp = float(value)
    
