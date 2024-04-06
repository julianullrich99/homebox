from queue import Queue
import RPi.GPIO as GPIO
from pwmPCA9685 import pwm as pwm
import time
import threading

from queueRunner import QueueRunner

class lightOneChannel(QueueRunner, threading.Thread, ):
    def __init__(self, config = {}, name="WhiteThread"):
        threading.Thread.__init__(self, name=name)

        self.queue = Queue()

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

        self.externalDimState = 'OFF'
        self.externalDimUpdateTime = 0

        self.morphingTime = 1000 if 'morphingTime' not in config else config['morphingTime']
        self.morphingSteps = max(2, int(self.morphingTime/10))

    def run1(self):
        while True:
          QueueRunner.run(self, nowait=True, loop=False)
          # self.externalDimRunner()
          time.sleep(0.1)
          if (self.externalDimState != 'OFF' and  (time.time() - self.externalDimUpdateTime) > 0.1): # incase of connection loss
              print('resetting external dim state')
              self.externalDimState = 'OFF'

    def externalDimInput(self, value):
      # print('setting dim state '+value)
      self.externalDimState = value
      self.externalDimUpdateTime = time.time()

    def externalDimRunner(self):
        # print('running dim runner')
        if(self.externalDimState == 'OFF'): return

        starttime = time.time()
        while (self.externalDimState == 'ON' or self.externalDimState == 'HOLD'):
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
        while (self.externalDimState == 'ON' or self.externalDimState == 'HOLD'):
            if (self.externalDimState != 'OFF' and  (time.time() - self.externalDimUpdateTime) > 0.1): # incase of connection loss
                self.externalDimState = 'OFF'

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

    def dim(self,c):
        # global storeValue, strip, on, rise, channel, start, number, dimThreshold, startThreshold
        print("dim")
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
        if (value == 0):
            if not self.on:
                return
            else:
                for i in range(0, self.morphingSteps+1):
                    value = self.currVal*(self.morphingSteps-i)/self.morphingSteps
                    self.out.set(value)
                    time.sleep(0.005)
                self.on = False
                self.rise = True
                return
        else:
            if not self.on:
                self.currVal = value
                for i in range(0, self.morphingSteps+1):
                    value = self.currVal*i/self.morphingSteps
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
      self.queue.put({'f':self.morphto, 'a': [int(value)]})

    def setToggle(self,value):
        if self.on:
            self.morphto(0)
        else:
            self.morphto(255)


    def setJarvis(self,value):
        value = value.decode("utf-8")
        print("setJarvis: ",value)
        if (value == "on"):
            self.morphto(100)
        elif (value == "off"):
            self.morphto(0)
