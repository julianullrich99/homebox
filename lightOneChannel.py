
import RPi.GPIO as GPIO
from pwmPCA9685 import pwm as pwm
import time
import threading

class lightOneChannel(threading.Thread):
    def __init__(self, config = {}, name="WhiteThread"):
        threading.Thread.__init__(self, name=name)

        self.inputPin = -1
        if 'dimInput' in config:
            self.inputPin = config['dimInput']
            GPIO.setup(self.inputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(self.inputPin, GPIO.RISING, callback=self.dim)


        self.out = pwm(config['output'],255)

        self.currVal = 0 # 0-255

        self.dimThreshold = 0.5
        self.startThreshold = 0.05

        self.on = False
        self.rise = True

    def dim(self,c):
        # global storeValue, strip, on, rise, channel, start, number, dimThreshold, startThreshold
        print "dim"
        starttime = time.time()
        while GPIO.input(self.inputPin):
            time.sleep(0.02)
            if time.time() - starttime >= 0.5:
                break
        endtime = time.time()
        timediff = endtime-starttime
        if timediff < self.startThreshold:
            return 0
        if timediff < self.dimThreshold:
            if not self.on:
                for i in range(0,101):
                    value = (self.currVal*i/100)
                    # print value
                    self.out.set(value)
                    time.sleep(0.005)
                self.on = not self.on
            else:
                for i in range(0,101):
                    value = (self.currVal*(100-i)/100)
                    # print value
                    self.out.set(value)
                    time.sleep(0.005)
                self.on = not self.on
        else:
            if not self.on:
                self.currVal = 0
        while GPIO.input(self.inputPin):
            if self.rise:
                if self.currVal < 255:
                    self.currVal += 1
            else:
                if self.currVal > 0:
                    self.currVal -= 1
            value = (self.currVal)
            # print value
            self.out.set(value)
            if self.currVal == 0:
                self.on = False
                self.currVal = 50
                break
            else:
                self.on = True
            time.sleep(0.015)
        self.rise = not self.rise

    def morphto(self,value):
        print "morphing to",value
        if (value == 0):
            if not self.on:
                return
            else:
                for i in range(0,101):
                    value = self.currVal*(100-i)/100
                    # print value
                    self.out.set(value)
                    time.sleep(0.005)
                self.on = False
                self.rise = True
                return
        else:
            if not self.on:
                self.currVal = value
                for i in range(0,101):
                    value = self.currVal*i/100
                    # print value
                    self.out.set(value)
                    time.sleep(0.005)
                self.on = True
                return
            if (value > 127):
                self.rise = False
            else:
                self.rise = True

        start = self.currVal
        d1 = int(value) - start

        n = 100
        speed = 1
        for counter in range(0, n + 1):
            self.currVal = start + (counter * d1 / 100)
            self.out.set(self.currVal)
            time.sleep(float(speed)/n)

    def set(self, value):
        if (value == 0):
            if not self.on:
                return
            else:
                self.out.set(value)
                self.on = False
                self.rise = True
                return
        else:
            if not self.on:
                self.currVal = value
                self.out.set(value)
                self.on = True
            if (value > 127):
                self.rise = False
            else:
                self.rise = True
        return

    def setMQTT(self,value):
        self.morphto(int(value))