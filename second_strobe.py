import time
import board
import neopixel
import asyncio
import math

pixels = neopixel.NeoPixel(board.D18, 60)

class Led(object):
    def __init__(self, n=0):
        self.r = 0
        self.g = 0
        self.b = 0
        self.n = n

    def getRGB(self):
        return (self.r, self.g, self.b)

    async def setRGB(self):
        pixels[self.n] = await self.getRGB()

    async def strobeRed(self):
        self.r = 50
        while self.r > 0:
            self.r = self.r - 1
            self.setRGB(n)
            await asyncio.sleep(0.05)

class LedStrip(object):
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0
        self.pixels = neopixel.NeoPixel(board.D18, 60)

    def getRGB(self):
        return (self.r, self.g, self.b)

    def setRGB(self, n):
        self.pixels[n] = self.getRGB()

    async def strobeRed(self, n, t=0.01):
        self.r = 50
        await self.setRGB(n)
        while self.r > 0:
            self.r -= 1
            await self.setRGB(n)
            await asyncio.sleep(t)

    async def strobeRedAll(self):
        for i in range(60):
            await self.strobeRed(i)
            await self.strobeRed(i+1, 0.05)

    def sineAll(self):
        self.t = 0
        self.active = True
        while self.active:
            try:
                for i in range(60):
                    pixels[i] = (
                        # int(50 * math.sin(self.t + i / 2) ** 2),
                        # int(250 * math.sin(self.t - i / 2) ** 2),
                        0,
                        int(100 * math.sin(self.t + 2 * i / 2) ** 2),
                        int(255 * math.sin(self.t + 2 * i / 2) ** 2))
                    self.t += 0.1
                    # time.sleep(0.001)
            except KeyboardInterrupt:
                self.active = False