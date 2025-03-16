import asyncio
import logging
import time
import logging.handlers as handlers
from importlib import import_module
from pymongo import MongoClient
from os import listdir, path
from dotenv import load_dotenv
from pyrogram import Client
from config2 import API_ID, API_HASH, BOT_TOKEN2, BOT_USERNAME, MONGO_URI




loop = asyncio.get_event_loop()
load_dotenv()
boot = time.time()


logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(stream=sys.stdout),
              handlers.RotatingFileHandler("zenova.log", mode="a", maxBytes=104857600, backupCount=2, encoding="utf-8")],)




zenova = Client(
    ":zenova:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN2,
)


client = MongoClient(MONGO_URI)
db = client["giveaway_db"]
giveaways = db["giveaways"]


async def zenova_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await zenova.start()
    getme = await zenova.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name


import asyncio
import importlib
from pyrogram import idle
from zenova import zenova
from modules import ALL_MODULES

loop = asyncio.get_event_loop()

async def zenova_boot():
    for all_module in ALL_MODULES:
        importlib.import_module("modules." + all_module)
    print("𝖻𝗈𝗍 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅 𝗌𝗍𝖺𝗋𝗍")
    await idle()
    print("Caught an unknown error")

