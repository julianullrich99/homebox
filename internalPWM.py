from queue import Queue
import RPi.GPIO as GPIO
from pwmPCA9685 import pwm as pwm
import time
import threading

from queueRunner import QueueRunner

class internalPWM(QueueRunner, threading.Thread, ):
    def __init__(self, config = {}, name="WhiteThread"):
        threading.Thread.__init__(self, name=name)

        self.queue = Queue()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config['output'], GPIO.OUT)

        startValue = int(config.get('startValue', 0))

        self.out = GPIO.PWM(config['output'],config['freq'])
        self.outPin = config['output']
        self.out.start(startValue)

        self.currVal = 0

    def run1(self):
        while True:
          QueueRunner.run(self, nowait=True, loop=False)
          time.sleep(0.1)

    def set(self, value: float):
      self.out.ChangeDutyCycle(value)
      print('setting', self.outPin,'to', value)

    def setMQTT(self,value):
      self.queue.put({'f':self.set, 'a': [int(value)/2.55]})
