from bot import Bot
from zenova import zenova_boot, zenova_bot
import asyncio

loop = asyncio.get_event_loop()

loop.run_until_complete(zenova_bot())
bot = Bot()
loop.run_until_complete(bot.start())
loop.run_until_complete(zenova_boot())

# from bot import Bot
# from zenova import zenova_boot, zenova_bot
# import asyncio

# async def main():
#     await zenova_bot()
#     bot = Bot()
#     await bot.start()
#     await zenova_boot()

# asyncio.run(main())