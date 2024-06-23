import asyncio
from bot import Bot
from zenova import zenova_boot, zenova_bot

if __name__ == "__main__":
    # Create separate event loops for each bot
    bot_loop = asyncio.new_event_loop()
    zenova_loop = asyncio.new_event_loop()
    

    async def run_bot():
        bot = Bot()
        await bot.run()

    # Start both bots in separate event loops
    zenova_loop.create_task(zenova_boot())
    zenova_loop.create_task(zenova_bot())
    bot_loop.create_task(run_bot())

    # Run both event loops concurrently
    asyncio.gather(zenova_loop.run_forever())