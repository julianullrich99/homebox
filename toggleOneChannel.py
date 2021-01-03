import RPi.GPIO as GPIO
from pwmPCA9685 import pwm as pwm
import time
import threading

class toggleOneChannel(threading.Thread):
    def __init__(self, config = {}, name="pump"):
        threading.Thread.__init__(self, name=name)

        self.out = pwm(config['output'],255)

        self.tempTimer = -1
        self.timer = -1
        if 'timer' in config:
            self.timer = config['timer']

        self.on = False

    def set(self, value):
        print("setting channel (pump)")
        if (value == 1):
            self.on = True
            self.out.set(255)
            if (self.timer != -1):
                self.startTimer()
        else:
            self.on = False
            self.out.set(0)
            if (self.tempTimer != -1):
                self.timer = self.tempTimer
                self.tempTimer = -1
        return

    def setMQTT(self,value,timer=-1):
        self.set(int(value))

    def setScheduler(self,timer):
        if (timer != -1):
            self.tempTimer = self.timer
            self.timer = timer
        self.set(1)

    def startTimer(self):
        start = time.time()
        while (time.time() < start + self.timer):
            time.sleep(0.1)
        self.set(0)
