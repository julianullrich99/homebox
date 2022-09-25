
class externalMQTT():
    def __init__(self,client,config):
        self.config = config
        self.client = client

        self.defaultTopic = ''

        if 'defaultTopic' in self.config:
            self.defaultTopic = self.config['defaultTopic']
        
    def send(self,data,topic = ""):
        if topic == "":
            topic = self.defaultTopic
        self.client.publish(topic,data,1,False)
