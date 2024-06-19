from bot import Bot
from zenova import zenova_boot, zenova_bot
import asyncio

loop = asyncio.get_event_loop()


loop.run_until_complete(zenova_bot())
Bot().run()
loop.run_until_complete(zenova_boot())