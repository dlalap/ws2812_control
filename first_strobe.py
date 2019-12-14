import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 60)

programActive = True
alt = False
i = 0
while programActive:
    try:
        if i % 2 == 0:
            if alt:
                pixels[i] = (0, 255, 0)
            else:
                pixels[i] = (50, 0, 0)
        else:
            if alt:
                pixels[i] = (50, 0, 0)
            else:
                pixels[i] = (0, 255, 0)
        i += 1
        if i == 60:
            i = 0
            alt = not alt
        time.sleep(0.02)
    except KeyboardInterrupt:
        programActive = False