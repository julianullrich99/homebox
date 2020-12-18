import time
import threading

class taskMultiplier():
    def __init__(self, config = {}):

        self.config = config

    def multiply(self, value):
        for fixture in self.config.outputs:
            val = value
            if (type(fixture.conversion).__name__ == "function"):
                val = fixture.conversion(value)

            func = threading.Thread(target=fixture.setFunction, args=(val,))
            func.start()


    def setMQTT(self,mqttValue):
        self.multiply(mqttValue)



