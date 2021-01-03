from __future__ import division
import socket
import threading
import time
import sys
import RPi.GPIO as GPIO
import json
import signal
import traceback
import paho.mqtt.client as mqtt
from apscheduler.schedulers.background import BackgroundScheduler
import code
from pytz import timezone
import datetime
import math
import telnetlib
from io import BytesIO
from cgi import parse_header, parse_multipart

from urllib.parse import parse_qs

from http.server import BaseHTTPRequestHandler, HTTPServer

from neopixel import neopixelThread as zoe
from pwmPCA9685 import pwm as pwm
from lightOneChannel import lightOneChannel
from lightRGB import lightRGB
from toggleOneChannel import toggleOneChannel
from heaterControl import heaterControl
from jarvisParser import jarvisParser
from relayOneChannelMQTT import switchMQTT
import msc

jarvisParser = jarvisParser()

import colorHelper

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

hostName = ""
serverPort = 8080

def createLight(config):
    obj = config['class'](config['config'])
    obj.setDaemon(True)
    obj.start()
    if 'topics' in config:
        for topic in config['topics']:
            mqttTopics.append({'topic':topic['topic'],'callback':obj.__getattribute__(topic['callback'])})
    return obj

mqttTopics = []
objects = {}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    for entry in mqttTopics:
        client.subscribe(entry['topic'])
        print("subscribing to",entry['topic'])

    client.subscribe("jarvis/#")

 
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if (msg.topic.startswith("jarvis/")):
        t, v = jarvisParser.parse(msg.payload,msg.topic)

        print(t,v)
        client.publish("julian/"+t,v)

    for entry in mqttTopics:
        if (msg.topic == entry['topic']):
            entry['callback'](msg.payload)

def calc(x):
    #return 0.9784889413 * math.pow(1.021983957,x) - 1
    #return 0.9784889413 * math.exp(0.0217457939 * x)
    return x

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

class mqttThread(threading.Thread):
    def __init__(self, name='MQTTThread'):
        threading.Thread.__init__(self, name=name)
        client.connect("127.0.0.1", 1883, 60)
        self.sunriseEn = threading.Event()

    def run(self):
        client.loop_forever()

    def sunrise(self,data={"duration": 1800, "color": [100,53,30]}):
        self.sunriseEn.set()
        n = 100
        timesleep = float(data['duration'] / n * 4)
        print("duration: ",data['duration'])
        for i in range(1,n+1):
            if not self.sunriseEn.isSet():
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

    def stopSunrise(self):
        self.sunriseEn.clear()

class EventEngine():
    def __init__(self):
        self.timezone = timezone("Europe/Berlin")
        self.scheduler = BackgroundScheduler(timezone=self.timezone)
        self.scheduler.add_jobstore('sqlalchemy', url='sqlite:///schedule.sqlite')
        self.scheduler.start()

        # job = self.scheduler.add_job(testCallback, 'interval', hours=2, id='2', replace_existing=True, name="intervaltest")
        # job2 = self.scheduler.add_job(parse, 'cron', hour=5, minute=45, end_date='2019-05-08', id='1', replace_existing=True, name="wecker", args=['{"type":"mqtt","action":"sunrise","data":{"duration":1800,"color":[100,52,30]}}'])
        # job3 = self.scheduler.add_job(testCallback, 'date', run_date='2019-11-17 20:30:0', id='3', replace_existing=True)

    def getJobs(self):
        jobArr = self.scheduler.get_jobs()
        responseArr = []
        for job in jobArr:
            newJob = {}
            newJob["id"] = job.id
            newJob["name"] = job.name
            newJob["args"] = job.args
            newJob["running"] = False if (job.next_run_time == None) else True
            if hasattr(job.trigger, 'interval'):
                newJob['trigger'] = 'interval'
                newJob['triggerargs'] = {}
                newJob['triggerargs']['jitter'] = job.trigger.jitter
                newJob['triggerargs']['start_date'] = str(job.trigger.start_date)
                newJob['triggerargs']['end_date'] = str(job.trigger.end_date)
                interval = job.trigger.interval_length
                weeks = interval // (7*24*60*60)
                days = (interval - weeks * (7*24*60*60)) // (24*60*60)
                hours = (interval - weeks * (7*24*60*60) - days * (24*60*60)) // (60*60)
                minutes = (interval - weeks * (7*24*60*60) - days * (24*60*60) - hours * (60*60)) // 60
                seconds = (interval - weeks * (7*24*60*60) - days * (24*60*60) - hours * (60*60) - minutes * (60))
                newJob['triggerargs']['weeks'] = weeks
                newJob['triggerargs']['days'] = days
                newJob['triggerargs']['hours'] = hours
                newJob['triggerargs']['minutes'] = minutes
                newJob['triggerargs']['seconds'] = seconds
            if hasattr(job.trigger, 'fields'):
                newJob['trigger'] = 'cron'
                newJob['triggerargs'] = {}
                newJob['triggerargs']['jitter'] = job.trigger.jitter
                newJob['triggerargs']['start_date'] = str(job.trigger.start_date)
                newJob['triggerargs']['end_date'] = str(job.trigger.end_date)
                for field in job.trigger.fields:
                    newJob['triggerargs'][field.name] = str(field)
            if hasattr(job.trigger, 'run_date'):
                newJob['trigger'] = 'date'
                newJob['triggerargs'] = {}
                newJob['triggerargs']['run_date'] = str(job.trigger.run_date)
            responseArr.append(newJob)
        responseJson = json.dumps(responseArr)
        return responseJson

    def newJob(self,jsondata):
        data = json.loads(jsondata)
        triggerargs = data['triggerargs']
        # code.interact(local=locals())
        self.scheduler.add_job(runScheduled, data['trigger'], id=data['id'], replace_existing=True, name=data['name'], args=[data['object'],data['args'][0]], **triggerargs)

        # if (data['trigger'] == 'cron'):
        #     self.scheduler.add_job(parse, data['trigger'], id=data['id'], replace_existing=True, name=data['name'], args=[json.dumps(data['args'][0])], jitter=triggerargs['jitter'], year=triggerargs['year'], month=triggerargs['month'], week=triggerargs['week'], day=triggerargs['day'], day_of_week=triggerargs['day_of_week'], hour=triggerargs['hour'], minute=triggerargs['minute'], second=triggerargs['second'], start_date=triggerargs['start_date'], end_date=triggerargs['end_date'])
        # if (data['trigger'] == 'interval'):
        #     self.scheduler.add_job(parse, data['trigger'], id=data['id'], replace_existing=True, name=data['name'], args=[json.dumps(data['args'][0])], jitter=triggerargs['jitter'], weeks=triggerargs['week'], days=triggerargs['day'], hours=triggerargs['hour'], minutes=triggerargs['minute'], seconds=triggerargs['second'], start_date=triggerargs['start_date'], end_date=triggerargs['end_date'])
        # if (data['trigger'] == 'date'):
        #     self.scheduler.add_job(parse, data['trigger'], id=data['id'], replace_existing=True, name=data['name'], args=[json.dumps(data['args'][0])], run_date=triggerargs['run_date'])

    def deleteJob(self,jobid):
        self.scheduler.remove_job(jobid)

    def toggleJob(self,jobId):
        print("toggle")
        if (self.scheduler.get_job(jobId).next_run_time == None):
            #unpause job
            self.scheduler.resume_job(jobId)
        else:
            #pause job
            self.scheduler.pause_job(jobId)

    def newTimer(self,data):
        duration = data['time']
        id = data['id']
        run_date = datetime.datetime.fromtimestamp(math.floor(time.time() + int(duration)),self.timezone).isoformat()
        self.scheduler.add_job(alarm, 'date', run_date=run_date, id=id, replace_existing=True, name="Clock_alarm")

    def stopTimer(self,data):
        id = data['id']
        try:
            self.scheduler.remove_job(id)
        except Exception as e:
            pass
        alarmStop.set()

nightlightChain = createLight({
        'class': lightOneChannel,
        'config': {
            'output': 3,
            'dimInput': 18
        },
        'topics': [
            {
                'topic':'julian/nightlightChain',
                'callback':'setMQTT'
            }
        ]
    })

deskLight = createLight({
        'class': lightOneChannel,
        'config': {
            'output': 2
        },
        'topics': [
            {
                'topic':'julian/deskLight',
                'callback':'setMQTT'
            }
        ]
    })

bedLight = createLight({
        'class': lightRGB,
        'config': {
            'output': {
                'r': 4,
                'g': 5,
                'b': 6
            },
            'dimInput': 22,
            'dimColor': [127,0,255],
            'dimBrightness': 100
        },
        'topics': [
            {
                'topic':'julian/bedLight',
                'callback':'setMQTT'
            }
        ]
    })

ambilight = createLight({
        'class': lightRGB,
        'config': {
            'output': {
                'r': 8,
                'g': 9,
                'b': 10
            },
        },
        'topics': [
            {
                'topic':'julian/ambiLight',
                'callback':'setMQTT'
            }
        ]
    })

whiteboardLight = createLight({
        'class': lightRGB,
        'config': {
            'output': {
                'r': 13,
                'g': 11,
                'b': 12
            },
        },
        'topics': [
            {
                'topic':'julian/whiteboardLight',
                'callback':'setMQTT'
            }
        ]
    })

underbedLight = createLight({
        'class': lightRGB,
        'config': {
            'output': {
                'r': 14,
                'g': 15,
                'b': 16
            },
        },
        'topics': [
            {
                'topic':'julian/underbedlight',
                'callback':'setMQTT'
            }
        ]
    })

objects['waterpump'] = createLight({
        'class': toggleOneChannel,
        'config': {
            'output': 7,
            'timer': 5
        },
        'topics': [
            {
                'topic':'julian/waterpump',
                'callback':'setMQTT'
            }
        ]
    })

mainLight = createLight({
        'class': switchMQTT,
        'config': {
            'mqttClient': client,
            'switchTopic': 'sonoff/mainLight/cmnd/tasmota_switch/Power'
        },
        'topics': [
            {
                'topic': 'julian/mainLight',
                'callback': 'setMQTT'
            },
            {
                'topic': 'julian/lichtschalter1',
                'callback': 'switch'
            }
        ]
    })

neopixel = createLight({
        'class': zoe,
        'config': { },
        'topic': 'julian/zoeRainbow',
        'topics': [
            {
                'topic':'julian/zoeRainbow',
                'callback':'setMQTT'
            },
            {
                'topic':'julian/zoeColor',
                'callback':'setColorMQTT'
            },
            {
                'topic':'julian/zoeListening',
                'callback':'zoeSetListening'
            },
            {
                'topic':'jarvis/recording',
                'callback':'zoeSetListening'
            }
        ]
    })

objects['fullLightMultiplier'] = createLight({
    'class':msc.taskMultiplier,
    'config': {
        'outputs': [
            {
                'setFunction': ambilight.setMQTT,
                'conversion': None
            },
            {
                'setFunction': bedLight.setMQTT,
                'conversion': None
            },
            {
                'setFunction': neopixel.setColorMQTT,
                'conversion': None
            },
            {
                'setFunction': underbedLight.setMQTT,
                'conversion': None
            },
            {
                'setFunction': whiteboardLight.setMQTT,
                'conversion': None
            },
        ]
    },
    'topics': [
        {
            'topic':'julian/fullLight',
            'callback':'setMQTT'
        }
    ]
    })

objects['heater'] = createLight({
        'class': heaterControl,
        'config': {
            'mqttClient': client,
            'switchTopic': 'sonoff/heizung/cmnd/tasmota_switch/Power',
            'sensorPin': 5,
            'metricTopic': 'julian/currTemp',
        },
        'topics': [
            {
                'topic': 'julian/heizung',
                'callback': 'setMQTT'
            }
        ]
    })

#objects['fullLightSunrise'] = createLight({
        #'class':msc.sunrise,
        #'config': {
            #'callback': objects['fullLightMultiplier'].setMQTT,
            #'outputColorFormat': '888',
            #'time': 1800,
            #'color': [255,255,255]
        #}

    #})

tmqtt = mqttThread()
tmqtt.setDaemon(True)
tmqtt.start()

# tneopixel = neopixelThread()
# tneopixel.setDaemon(True)
# tneopixel.start()

def parse(data,conn=None):
    print("Parsing: ",data)
    jsonobj = json.loads(data)
    response = ""
    if 'type' not in jsonobj and 'entities' in jsonobj:
        arr = {}
        for index in jsonobj['entities']:
            arr[index] = jsonobj['entities'][index][0]['value']
        parse(json.dumps(arr))
        return
    if jsonobj['type'] == 'neopixel':
        if jsonobj['action'] == 'zoeStartRainbow':
            response = tneopixel.zoeStartRainbow()
            print('startRainbow')
        if jsonobj['action'] == 'zoeStopRainbow':
            response = tneopixel.zoeStopRainbow()
            print('stopRainbow')
        if jsonobj['action'] == 'zoeBrightness':
            response = tneopixel.zoeBrightness(jsonobj["value"])
            print('zoeBrightness')
    if jsonobj['type'] == "schedule":
        if jsonobj['action'] == "getJobs":
            response = events.getJobs()
        if jsonobj['action'] == "newJob":
            events.newJob(jsonobj['data'])
            response = '{"status":"success"}'
        if jsonobj['action'] == "deleteJob":
            events.deleteJob(jsonobj['data'])
            response = '{"status":"success"}'
        if jsonobj['action'] == "toggleJob":
            events.toggleJob(jsonobj['data'])
            response = '{"status":"success"}'
        if jsonobj['action'] == "newTimer":
            events.newTimer(jsonobj['data'])
            response = '{"status":"success"}'
        if jsonobj['action'] == "stopTimer":
            events.stopTimer(jsonobj['data'])
            response = '{"status":"success"}'
        if conn is not None:
            conn.send(response)
    if 'respId' in jsonobj:
        # print jsonobj['respId']
        client.publish("julian/redding/response/"+jsonobj['respId'],response,1,False)

def runScheduled(objectName, args):
    objects[objectName].setScheduler(*json.loads(args))


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if "getJobs" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(events.getJobs(),"utf-8"))
        else:    
            if self.path == "/":
                self.path = "/index.php"
            try:
                with open(self.path[1:]) as file:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes(file.read(),"utf-8"))
            except:
                self.send_response(404)
                self.end_headers()

   
    
    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        if self.headers['Content-Type'] != "application/json":
            self.wfile.write(b"only accepting JSON")
            return

        # postvars = self.parse_POST()
        body = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(body.decode("utf-8"))

        if "deleteJob" in self.path:
            events.deleteJob(data['id'])
            pass
        elif "newJob" in self.path:
            events.newJob(data['data'])
        elif "toggleJob" in self.path:
            events.toggleJob(data['id'])
            


def main():
    webServer = HTTPServer((hostName, serverPort), MyServer)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

events = EventEngine()

main()
