from queue import Queue
import re
import threading
from queueRunner import QueueRunner

class runtimeConfigurableMatrix(QueueRunner, threading.Thread):
    def __init__(self,config = {}, name=""):
      threading.Thread.__init__(self, name=name)
      threading.excepthook = print

      self.queue = Queue()

      self.actions = config['actions']
      self.matrix = config['templates']['default']
      self.templates = config['templates']

    def handle(self, value, topic):
      if not topic in self.matrix:
        return

      topicConfig = self.matrix[topic]
      print(topicConfig)

      for entry in topicConfig:
        if re.search(topicConfig[entry]['msg'], value):
          action = topicConfig[entry]['action']
          self.executeAction(action, value)
          return

    def executeAction(self, action, value):
      if not action in self.actions:
        return
      
      resolvedAction = self.actions[action]

      val = value
      if (type(resolvedAction['conversion']).__name__ == "function"):
        val = resolvedAction['conversion'](value)

      resolvedAction['target']['fixture'].__getattribute__(resolvedAction['target']['method'])(val)

    def setMQTT(self, value, topic):
      self.queue.put({ 'f':self.handle, 'a':[value, topic] })
