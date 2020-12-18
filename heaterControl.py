import threading
import time
import datetime

import dht11
import externalMQTT
import average
import loggingclass as logging

class heaterControl(threading.Thread):
    def __init__(self,config = {}, name=""):
        threading.Thread.__init__(self, name=name)

        self.targetTemp = 0
        self.currentTemp = 1
        self.heating = 0
        self.checkInterval = 20 # checkintervall in sekunden (auch fürs logging)

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

        self.logger = logging.logging("csv",{"outputFile":"tempData.csv","format":["time","currTemp","targetTemp","humidity","heating"]})

    def run(self):
        while True:
            data = self.sensor.read()
            print(data)

            self.currentTemp = self.averageTemp.get(data['temp'])
            hum = self.averageHum.get(data['hum'])

            self.logger.log({
                    'time':datetime.datetime.now().isoformat(),
                    'currTemp': self.currentTemp,
                    'targetTemp': self.targetTemp,
                    'humidity': hum,
                    'heating': self.heating
                },"temp") 

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
    
