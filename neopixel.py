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
                self.zoeMorphto(self.zoeColor,self.zoeOldColor)
                self.zoeOldColor = self.zoeColor

            elif (self.zoeRainbowEn.isSet()):
                self.zoeRainbow()

            elif (self.zoeColor == [0,0,0]):
                self.overrideDark()

            time.sleep(0.1)

    def zoeStartRainbow(self):
        self.zoeRainbowEn.set()

    def zoeStopRainbow(self):
        self.zoeRainbowEn.clear()

    def zoeBrightness(self,value):
        self.zoeBrightness = value

    def zoeSetColor(self,color):
        self.zoeColor = color
        self.zoeRainbowEn.clear()
        self.zoeChangeEvent.set()

    def zoeRainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            for i in range(self.zoePixels):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.zoePixels) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)
            if not self.zoeRainbowEn.isSet():
                self.zoeMorphto([0,0,0],[0,0,0],0,1)
                break
    
    def overrideDark(self):
        for i in range(self.zoePixels):
            self.strip.setPixelColor(i, Color(0,0,0))
        self.strip.show()
    
    def zoeMorphto(self,color,start,speed=1,n=100):
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
                self.strip.setPixelColor(i, Color(int(r1_end),int(g1_end),int(b1_end)))
            self.strip.show()
            time.sleep(float(speed)/n)
        self.zoeChangeEvent.clear()

    def wheel(self,pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(int(pos * 3 * float(self.zoeBrightness/255)), int((255 - pos * 3) * float(self.zoeBrightness/255)), 0)
        elif pos < 170:
            pos -= 85
            return Color(int((255 - pos * 3) * float(self.zoeBrightness/255)), 0, int(pos * 3 * float(self.zoeBrightness/255)))
        else:
            pos -= 170
            return Color(0, int(pos * 3 * float(self.zoeBrightness/255)), int((255 - pos * 3) * float(self.zoeBrightness/255)))

    def setMQTT(self,mqttVal):
        if (mqttVal == b'1'):
            self.zoeStartRainbow()
        else:
            self.zoeStopRainbow()

    def setColorMQTT(self,val):
        color = colorHelper.convertColor(val.decode('utf-8'),"888")
        self.zoeSetColor(color)