from bot import Bot
from zenova import zenova_boot, zenova_bot
import asyncio
import threading

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    bot_thread = threading.Thread(target=Bot().run)
    bot_thread.start()
    loop.run_until_complete(asyncio.gather(zenova_bot(), zenova_boot()))
