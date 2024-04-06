import time
import threading


class bedAutoShutoff(threading.Thread, ):
    def __init__(self, config = {}, name="WhiteThread"):
        threading.Thread.__init__(self, name=name)

        self.client = config['client']
        self.triggerTime = 20
        self.isOver30 = False
        self.timeOver30 = None
        self.timeUnder30 = None
    
    def run(self):
        while True:
            time.sleep(10)
            current_time = time.time()

            if self.isOver30 and self.timeUnder30 is not None and current_time - self.timeUnder30 >= self.triggerTime:
                self.isOver30 = False
                print('Triggering over30: False')
                self.client.publish('julian/bedPump', 0)
                self.client.publish('julian/bedFan', 0)
                self.client.publish('julian/bedPeltier', 0)

    def handleNewMessage(self, msg: str, topic: str):
        temp = float(msg)

        if temp > 30:
          if not self.isOver30:
            self.isOver30 = True
            print('Triggering over30: True immediately as temp is over 30')
          self.timeUnder30 = None

        elif temp < 30:
          if self.timeUnder30 is None:
            self.timeUnder30 = time.time()
            print('Setting under 30 time')