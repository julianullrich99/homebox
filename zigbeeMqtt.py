import json
import threading
from externalMQTT import externalMQTT
from queueRunner import QueueRunner
from queue import Queue

class zigbeeMqtt(QueueRunner, threading.Thread):
    def __init__(self,config = {}, name=""):
        threading.Thread.__init__(self, name=name)
        threading.excepthook = print

        self.queue = Queue()

        self.target = externalMQTT({
            'defaultTopic': "zigbee2mqtt/" + config['name'] + "/set",
            'client': config['mqttClient']
        })
    
    def set(self, key, value):
      print("setting ZIGBEE", key, value)
      data = {}
      data[key] = value
      print(data)
      self.target.send(json.dumps(data))
      
    def setMQTT(self, value, topic):
      key = topic.split("/")[-1]
      self.queue.put({ 'f':self.set, 'a':[key, value] })
    
    def setObject(self, data):
      print("setObject", data)
      self.set(data['key'], data['value'])