import asyncio
from bot import Bot
from zenova import zenova_boot, zenova_bot

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    async def run_bot():
        bot = Bot()
        await bot.run()

    loop.run_until_complete(asyncio.gather(zenova_bot(), zenova_boot(), run_bot()))
