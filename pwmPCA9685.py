from __future__ import division
import time
from board import SCL, SDA
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 1000

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
        pca.channels[self.pin].duty_cycle = int(0xffff / self.res * val)
        time.sleep(0.0005)

class pwmRGB():
    def __init__(self,r,g,b,res=255):
        self.r = pwm(r,res)
        self.g = pwm(g,res)
        self.b = pwm(b,res)

    def set(self,val):
        self.r.set(val[0])
        self.g.set(val[1])
        self.b.set(val[2])
