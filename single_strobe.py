import time
import board
import neopixel
import asyncio

pixels = neopixel.NeoPixel(board.D18, 60)

programActive = True
alt = False
i = 0
while programActive:
    try:
        pixels[0] = (i, 0, 0)
        if alt:
            i -= 1
        else:
            i += 1
        
        if i >= 60 or i == 0:
            alt = not alt
        time.sleep(0.02)
    except KeyboardInterrupt:
        programActive = False