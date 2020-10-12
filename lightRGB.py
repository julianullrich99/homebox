
import RPi.GPIO as GPIO
from pwmPCA9685 import pwmRGB
import time
import threading
import colorHelper

class lightRGB(threading.Thread):
    def __init__(self, config = {}, name="WhiteThread"):
        threading.Thread.__init__(self, name=name)

        self.inputPin = -1
        self.dimColor = [0,0,0]
        self.dimBrightness = 255
        if "dimInput" in config:
            print("dimming activated")
            self.inputPin = config['dimInput']
            self.dimColor = config['dimColor']
            self.dimBrightness = config['dimBrightness']
            GPIO.setup(self.inputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(self.inputPin, GPIO.RISING, callback=self.dim)

        self.format = '888'

        self.out = pwmRGB(config['output']['r'],config['output']['g'],config['output']['b'])

        self.currVal = [0,0,0] 
        self.dimCounter = 0

        self.dimThreshold = 0.5
        self.startThreshold = 0.05

        self.on = False
        self.rise = True

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
            print("under startthreshold")
            return 0
        if timediff < self.dimThreshold:
            print("under dimthreshold")
            if not self.on:
                for i in range(0,101):
                    value = colorHelper.dimCalculator(self.currVal,colorHelper.dimCalculator([0,0,0],self.dimColor,self.dimBrightness,255),i,100)
                    # print value
                    self.out.set(value)
                    time.sleep(0.005)
                self.currVal = value
                self.on = True
                self.rise = False
                self.dimCounter = self.dimBrightness
            else:
                for i in range(0,101):
                    value = colorHelper.dimCalculator(self.currVal,[0,0,0],i,100)
                    # print value
                    self.out.set(value)
                    time.sleep(0.005)
                self.dimBrightness = colorHelper.getMax(self.currVal)
                self.currVal = value
                self.on = False
                self.rise = True
                self.dimCounter = 0
            return
            
        print("dimming now")
        while GPIO.input(self.inputPin):
            if self.rise:
                if self.dimCounter < 255:
                    self.dimCounter += 1
            else:
                if self.dimCounter > 0:
                    self.dimCounter -= 1


            if self.on:
                value = colorHelper.dimColor(self.currVal,self.dimCounter,255)
            else:
                value = colorHelper.dimColor(self.dimColor, self.dimCounter,255)

            # print("rise:",self.rise,"dimCounter:",self.dimCounter,"on:",self.on,"value:",value)

            self.out.set(value)

            if self.dimCounter == 0 or self.dimCounter == 255:
                break

            time.sleep(0.015)

        self.currVal = value

        if self.dimCounter != 0:
            self.on = True
        else:
            self.on = False

        self.rise = not self.rise

    def morphto(self,value):  # value = [255,255,255]
        print("morphing to",value)
        self.dimCounter = colorHelper.getMax(value)
        self.dimColor = colorHelper.normalizeColor(value)

        if (value == [0,0,0]):
            if not self.on:
                return
            else:
               self.rise = True
               self.on = False

        else:
            if (colorHelper.getMax(value) > 127):
                self.rise = False
            else:
                self.rise = True

            if not self.on:
               self.on = True

        start = self.currVal
        d = [value[0] - start[0], value[1] - start[1], value[2] - start[2]]

        n = 100
        speed = 1
        for counter in range(0, n + 1):
            self.currVal = [
                    start[0] + (counter * d[0] / 100),
                    start[1] + (counter * d[1] / 100),
                    start[2] + (counter * d[2] / 100)
                ]
            # self.out.r.set(self.currVal[0])
            # self.out.g.set(self.currVal[1])
            # self.out.b.set(self.currVal[2])
            self.out.set(self.currVal)
            time.sleep(float(speed)/n)

        return

    def set(self, value):
        if (value == [0,0,0]):
            if not self.on:
                return
            else:
                self.out.set(value)
                self.on = False
                self.rise = True
        else:
            if not self.on:
                self.out.set(value)
                self.currVal = value
                self.on = True

            if (colorHelper.getMax(value) > 127):
                self.rise = False
            else:
                self.rise = True
        return

    def setMQTT(self,invalue):
        value = colorHelper.convertColor(invalue,self.format)
        self.morphto(value)