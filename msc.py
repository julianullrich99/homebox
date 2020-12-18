import time
import threading

class taskMultiplier():
    def __init__(self, config = {}):

        self.config = config

    def multiply(self, value):
        for fixture in self.config['outputs']:
            print(fixture)
            val = value
            if (type(fixture['conversion']).__name__ == "function"):
                val = fixture['conversion'](value)

            func = threading.Thread(target=fixture['setFunction'], args=(val,))
            func.start()


    def setMQTT(self,mqttValue):
        self.multiply(mqttValue)

    def setDaemon(self,x):
        return # dummy function to emulate threading class
    
    def start(self):
        return

class sunrise(threading.Thread):
    def __init__(self, config = {}, name = ""):
        self.config = config
        self.stopEvent = threading.Event()
        self.startEvent = threading.Event()

    def run(self):
        """ main control loop """

        while True:
            if (self.stopEvent.isSet()):
                self.stopSunrise()

            elif (self.startEvent.isSet()):                    
                self.startSunrise()

            time.sleep(0.1)

    def startSunrise(self):
    #def sunrise(self,data={"duration": 1800, "color": [100,53,30]}):
        n = 100
        timesleep = float(self.config['time'] / n * 4)

        for i in range(1,n+1):

            if self.stopEvent.isSet():
                break

            color = ""
            color += "{:02x}".format(int(data['color'][0] * 2.55 * i / 100))
            color += "{:02x}".format(int(data['color'][1] * 2.55 * i / 100))
            color += "{:02x}".format(int(data['color'][2] * 2.55 * i / 100))
            newData = {"type": "mqtt", "action": "roomLight", "data": color}
            newData1 = {"type": "light", "action": "white", "data": i}
            parse(json.dumps(newData))
            parse(json.dumps(newData1))
            if (i == 10):
                timesleep = timesleep / 2.0
            if (i == 17):
                timesleep = timesleep / 2.0
            if (i == 34):
                timesleep = timesleep / 2.0
            print("i",i)
            print("sleeping", timesleep)
            time.sleep(timesleep)

    #def setScheduler(self,color = self.config['color'], time = self.config['time']):
        #self.config['color'] = color
        #self.config['time'] = time
        #self.stopEvent.clear()
        #self.startEvent.set()


