import time
import threading
import jarvisConfig as conf

class jarvisParser():

    def parse(self,value,topic):
        value = value.decode("utf-8")
        print("value:",value,"topic",topic)

        try:
        
            t = topic.split("/")[1]
            print("t",t)
    
            parse = conf.conf['topics'][t]
            print("parse",parse)

            top = parse['topic']
            print("top",top)
    
            v = conf.conf['types'][parse['type']][value]
            print("v",v)

            return (top,str(v))

        except:
            print("Not found")
