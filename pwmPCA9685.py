from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685

pwmModule = Adafruit_PCA9685.PCA9685(address=0x40)

pwmModule.set_pwm_freq(200)

def getPulseLengthForDutyCycle(cycle,max=255):
    # cycle is between 0 and max
    maxPulse = 4095
    pulse = maxPulse * cycle / max
    return int(pulse)

class pwm():
    def __init__(self,channel,res=255):
        self.pin = channel - 1 # 0 index
        self.res = res
        self.value = 0
        print("initializing pwm pin",channel)

    def set(self,val):
        pulse = getPulseLengthForDutyCycle(val,self.res)
        pwmModule.set_pwm(self.pin, 0, getPulseLengthForDutyCycle(val,self.res))
        time.sleep(0.0005)
