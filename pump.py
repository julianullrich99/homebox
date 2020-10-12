import RPi.GPIO as GPIO
from pwmPCA9685 import pwm as pwm
import time
import threading

class toggleOneChannel(threading.Thread):
    def __init__(self, config = {}, name="pump"):
        threading.Thread.__init__(self, name=name)

        self.out = pwm(config['output'],255)

        self.on = False

    def set(self, value):
        if (value == 1):
            self.on = True
            self.out.set(255)
        else:
            self.on = False
            self.out.set(0)
        return

    def setMQTT(self,value):
        self.set(int(value))