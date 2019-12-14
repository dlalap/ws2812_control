from second_strobe import LedStrip
import asyncio

strip = LedStrip()
# asyncio.run(strip.strobeRed(0))
# for i in range(60):
#     asyncio.run(strip.strobeRed(i))
# asyncio.run(strip.strobeRedAll())
strip.sineAll()