import time
import threading
from rpi_ws281x import PixelStrip, Color
import colorHelper

class neopixelThread(threading.Thread):
    def __init__(self, config = {}, name='NeopixelThread'):
        """ constructor, setting initial variables """
        threading.Thread.__init__(self, name=name)

        self._stopevent = threading.Event()

        self.zoeOldColor = [0,0,0]
        self.zoeColor = [0,0,0]

        self.zoeChangeEvent = threading.Event()
        self.zoeRainbowEn = threading.Event()
        self.zoePixels = 30
        self.zoeBrightness = 255

        self.rainbowRunning = False
        self.listeningRunning = False
        self.listeningAniEn = threading.Event()

        self.colors = []
        for i in range(self.zoePixels):
            self.colors.append([0,0,0])

        self.isMorphing = False
        self.tempcolors = []
        for i in range(self.zoePixels):
            self.tempcolors.append([0,0,0])

        # LED strip configuration:
        LED_COUNT      = 30      # Number of LED pixels.
        # LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
            # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def run(self):
        """ main control loop """

        while True:
            if (self.zoeChangeEvent.isSet()):
                self.zoeChangeEvent.clear()
                print('changeZoeColor')
                threading.Thread(target=self.morphAll, args=(1,)).start()
                self.zoeOldColor = self.zoeColor

            #elif (self.zoeRainbowEn.isSet() and not self.rainbowRunning):
                #äthreading.Thread(target=self.zoeRainbow, args=(self)).start()

            #elif (self.zoeColor == [0,0,0]):
                #self.overrideDark()

            self.showAll()

            time.sleep(0.01)

    def showAll(self):
        #print("showing colors:",self.colors[0],self.colors[1],self.colors[2])
        for i in range(self.zoePixels):
            if self.isMorphing:
                color = self.tempcolors[i]
            else:
                color = self.colors[i]

            self.strip.setPixelColor(i, Color(color[0],color[1],color[2]))
        self.strip.show()

    def zoeStartRainbow(self):
        self.zoeRainbowEn.set()
        threading.Thread(target=self.zoeRainbow, args=(self,)).start()
        self.morphAll(0)

    def zoeStopRainbow(self):
        self.zoeColor = [0,0,0]
        self.morphAll(1)
        self.zoeRainbowEn.clear()

    def zoeStartListening(self):
        self.zoeRainbowEn.clear()
        self.listeningAniEn.set()
        threading.Thread(target=self.listening, args=(self,)).start()
        self.morphAll(0)

    def zoeStopListening(self):
        self.zoeColor = [0,0,0]
        self.morphAll(1)
        self.listeningAniEn.clear()

    def zoeSetListening(self,value):
        if value == b'1':
            self.zoeStartListening()
        else:
            self.zoeStopListening()

    def zoeBrightness(self,value):
        self.zoeBrightness = value

    def zoeSetColor(self,color):
        self.zoeColor = color
        self.zoeRainbowEn.clear()
        self.zoeChangeEvent.set()

    def zoeSetFullColor(self,color):
        for i in range(self.zoePixels):
            self.colors[i]=color

    def zoeRainbow(self, this, wait_ms=20, iterations=1):
        this.rainbowRunning = True
        """Draw rainbow that uniformly distributes itself across all pixels."""
        while True:
            if not this.zoeRainbowEn.isSet():
                break
            for j in range(256*iterations):
                for i in range(this.zoePixels):
                    #self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.zoePixels) + j) & 255))
                    this.colors[i] = this.wheel((int(i * 256 / this.zoePixels) + j) & 255,"arr")
                #self.strip.show()
                time.sleep(wait_ms/1000.0)
                if not this.zoeRainbowEn.isSet():
                    this.rainbowRunning = False
                    break
    
    def listening(self, this, wait_ms=50, iterations=1):
        this.listeningRunning = True
        """Draw rainbow that uniformly distributes itself across all pixels."""
        while True:
            if not this.listeningAniEn.isSet():
                break
            for i in range(this.zoePixels):
                if not this.listeningAniEn.isSet():
                    break
                #self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.zoePixels) + j) & 255))
                this.colors[i] = [0,255,0]
                this.colors[(i-5+this.zoePixels)%this.zoePixels] = [0,0,0]
                time.sleep(wait_ms/1000.0)
            #self.strip.show()
            if not this.listeningAniEn.isSet():
                this.listeningRunning = False
                break
    
    def zoeMorphto(self,color,start,speed=0.5,n=100):
        print("foo")
        r1 = int(start[0])  # Anfangswerte
        g1 = int(start[1])
        b1 = int(start[2])

        dr1 = int(color[0]) - r1  # Differenz Ende - Anfang
        dg1 = int(color[1]) - g1
        db1 = int(color[2]) - b1

        n = 100
        speed = 1 # 1 sec
        for counter in range(0, n + 1):
            r1_end = r1 + (counter * dr1 / 100)
            g1_end = g1 + (counter * dg1 / 100)
            b1_end = b1 + (counter * db1 / 100)
            for i in range(self.zoePixels):
                #self.strip.setPixelColor(i, Color(int(r1_end),int(g1_end),int(b1_end)))
                self.colors[i] = [int(r1_end),int(g1_end),int(b1_end)]
            #self.strip.show()
            time.sleep(float(speed)/n)
        self.zoeChangeEvent.clear()

    def morphAll(self,direction=1,speed=0.5,n=100):
        self.isMorphing = True

        colorArr = self.colors
        color = self.zoeColor

        for counter in range(n):

            for i in range(len(colorArr)):
                if direction == 1: # vom array zur einzelnen farbe
                    r1 = int(colorArr[i][0])  # Anfangswerte
                    g1 = int(colorArr[i][1])
                    b1 = int(colorArr[i][2])

                    dr1 = int(color[0]) - r1  # Differenz Ende - Anfang
                    dg1 = int(color[1]) - g1
                    db1 = int(color[2]) - b1
                else:
                    r1 = int(color[0])  # Anfangswerte
                    g1 = int(color[1])
                    b1 = int(color[2])

                    dr1 = int(colorArr[i][0]) - r1  # Differenz Ende - Anfang
                    dg1 = int(colorArr[i][1]) - g1
                    db1 = int(colorArr[i][2]) - b1

                r1_end = r1 + (counter * dr1 / 100)
                g1_end = g1 + (counter * dg1 / 100)
                b1_end = b1 + (counter * db1 / 100)
                self.tempcolors[i] = [int(r1_end),int(g1_end),int(b1_end)]

            time.sleep(float(speed)/n)
            
        self.isMorphing = False
        if direction == 1:
            self.zoeSetFullColor(color)



    def wheel(self,pos,ret="color"):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            if ret == "color":
                return Color(int(pos * 3 * float(self.zoeBrightness/255)), int((255 - pos * 3) * float(self.zoeBrightness/255)), 0)
            elif ret == "arr":
                return [int(pos * 3 * float(self.zoeBrightness/255)), int((255 - pos * 3) * float(self.zoeBrightness/255)), 0]
        elif pos < 170:
            pos -= 85
            if ret == "color":
                return Color(int((255 - pos * 3) * float(self.zoeBrightness/255)), 0, int(pos * 3 * float(self.zoeBrightness/255)))
            elif ret == "arr":
                return [int((255 - pos * 3) * float(self.zoeBrightness/255)), 0, int(pos * 3 * float(self.zoeBrightness/255))]
        else:
            pos -= 170
            if ret == "color":
                return Color(0, int(pos * 3 * float(self.zoeBrightness/255)), int((255 - pos * 3) * float(self.zoeBrightness/255)))
            elif ret == "arr":
                return [0, int(pos * 3 * float(self.zoeBrightness/255)), int((255 - pos * 3) * float(self.zoeBrightness/255))]

    def setMQTT(self,mqttVal):
        if (mqttVal == '1'):
            self.zoeStartRainbow()
        else:
            self.zoeStopRainbow()

    def setColorMQTT(self,val):
        color = colorHelper.convertColor(val,"888")
        self.zoeSetColor(color)