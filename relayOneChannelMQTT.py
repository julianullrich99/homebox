from queue import Queue
import threading
import externalMQTT
import RPi.GPIO as GPIO
from queueRunner import QueueRunner

class switchMQTT(QueueRunner, threading.Thread):
    def __init__(self,config = {}, name=""):
        threading.Thread.__init__(self, name=name)
        threading.excepthook = print

        self.queue = Queue()

        self.inputPin = -1
        if 'input' in config:
            self.inputPin = config['input']
            GPIO.setup(self.inputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            print("inputPin für relay:",self.inputPin)
            GPIO.add_event_detect(self.inputPin, GPIO.FALLING, callback=self.switch)

        self.relay = externalMQTT.externalMQTT(config['mqttClient'], {
            'defaultTopic': config['switchTopic']
        })

        self.state = False
        self.timeout = False
        self.time = 500 # 500 ms

    def set(self, value):
        if (int( value ) == 1):
            self.state = True
        else:
            self.state = False

        self.relay.send(int(self.state))

    def switch(self,channel):
        # if self.timeout:
            # return

        self.state = not self.state
        self.relay.send(int(self.state))

        # self.timeout = True
        # time.sleep(self.time/1000)
        # self.timeout = False

    def setMQTT(self,value, topic):
        self.queue.put({ 'f':self.set, 'a':[value] })
