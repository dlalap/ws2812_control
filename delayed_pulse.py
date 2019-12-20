# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import threading
import random
import requests

class LedBulb():
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0

class LedStrip():
    def __init__(self, pixel_pin=board.D18, num_pixels=60):
        self.pixel_pin = pixel_pin
        self.num_pixels = num_pixels
        self.ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(
            self.pixel_pin,
            self.num_pixels,
            brightness=0.2,
            auto_write=False,
            pixel_order=self.ORDER
        )
        self.r = 0
        self.g = 0
        self.b = 0
        self.active = False

    def pulse(self, n):
        self.r = 255
        self.pixels[n] = (self.r, 0, 0)
        while self.r > 0:
            self.r -= 1
            self.pixels[n] = (self.r, 0, 0)
            self.pixels.show()

    def setRGB(self, n, s: tuple):
        self.pixels[n] = s

    def startStream(self):
        while True:
            for bulb in range(len(self.pixels)):
                self.pixels[bulb] = tuple([max(0, x - 5) for x in self.pixels[bulb]])
            self.pixels.show()
            time.sleep(0.001)

    def startStreamThread(self):
        self.backgroundThread = threading.Thread(name='background', target=self.startStream)

    def pulseThroughStrip(self, delayTime=0.5):
        bulbOn = 0
        continuousGreen = 0
        continuousBlue = self.num_pixels - 1
        prevTime = 0
        multiplier = 1
        self.active = True
        while self.active:
            for bulb in range(len(self.pixels)):
                self.pixels[bulb] = tuple([max(0, x - 5) for x in self.pixels[bulb]])

            if time.time() - prevTime >= delayTime:
                prevTime = time.time()
                self.pixels[bulbOn] = (
                    255, 
                    self.pixels[bulbOn][1],
                    self.pixels[bulbOn][2]
                    )

                bulbOn += multiplier * 1
                continuousGreen += 1
                continuousBlue -= 1

                self.pixels[(continuousGreen + round(self.num_pixels / 2)) % self.num_pixels] = (
                    self.pixels[(continuousGreen + round(self.num_pixels / 2)) % self.num_pixels][0],
                    255,
                    self.pixels[(continuousGreen + round(self.num_pixels / 2)) % self.num_pixels][2]
                )


                self.pixels[(continuousBlue)] = (
                    self.pixels[(continuousBlue)][0],
                    self.pixels[(continuousBlue)][1],
                    255
                )
            
                if bulbOn == 0 or bulbOn >= self.num_pixels - 1:
                    multiplier *= -1

                if continuousGreen > self.num_pixels - 1:
                    continuousGreen = 0

                if continuousBlue <= 0:
                    continuousBlue = self.num_pixels
                    
            self.pixels.show()
            
            time.sleep(0.001)
        self.active = False

    def singlePulseThroughStrip(self, delayTime=0.5):
        prevTime = 0
        self.active = True
        bulb = 0
        zeroArray = [(0, 0, 0) for x in range(self.num_pixels)]
        self.pixels[0] = (180, 180, 180)
        while list(self.pixels) != zeroArray:
            try:
                self.fadeOut()
                if time.time() - prevTime >= delayTime and bulb < 60:
                    prevTime = time.time()
                    self.pixels[bulb] = (180, 180, 180)
                    bulb += 1
                    if bulb == 30:
                        response = requests.get('http://192.168.1.252:5000/on')

                self.pixels.show()
                time.sleep(0.001)

            except KeyboardInterrupt:
                active = False
                self.clearPixels()
        self.active = False


    def fadeOut(self):
        for bulb in range(len(self.pixels)):
            self.pixels[bulb] = tuple([max(0, x - 3) for x in self.pixels[bulb]])

    def clearPixels(self):
        for bulb in range(len(self.pixels)):
            self.pixels[bulb] = (0, 0, 0)

    def randomSparks(self, delayTime=0.5):
        prevTime = 0
        self.active = True
        while self.active:
            # try:
                self.fadeOut()
                if time.time() - prevTime >= delayTime:
                    prevTime = time.time()
                    randBulb = random.randint(0, self.num_pixels-1)
                    self.pixels[randBulb] = (
                        195,
                        195,
                        195
                    )
                self.pixels.show()
                time.sleep(0.001)

            # except KeyboardInterrupt:
            #     self.clearPixels()
            #     self.pixels.show()

        self.active = False

if __name__ == '__main__':
    try:
        response = requests.get('http://192.168.1.252:5000/off')
        strip = LedStrip()
        # strip = LedStrip(board.D12, 12)
        # strip.pulseThroughStrip(0.01)
        strip.randomSparks(0.01)
        # strip.singlePulseThroughStrip(0.01)
        # strip.pixels.fill((195, 195, 195))
        # strip.pixels.show()
    except KeyboardInterrupt:
        response = requests.get('http://192.168.1.252:5000/on')
        strip.active = False
        strip.clearPixels()
        strip.pixels.show()