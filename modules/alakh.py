from pyrogram import filters
from pyrogram.types import Message

import aiohttp
from helper.prompts import alakh_ai
from zenova import zenova
import json


API_URL = "https://chatgpt.apinepdev.workers.dev/?question="

async def handle_alakh(message):
    txt = message
    async with aiohttp.ClientSession() as session:
         async with session.get(f"{API_URL}'prompt' :{alakh_ai},'user':{txt}") as response:
            data = await response.text()
            answer = json.loads(data)['answer']
            return answer


async def is_alakh(_, __, update: Message):
    return any(word in update.text.lower() for word in ['alakh'])
    
ALAKH = filters.create(is_alakh)

@zenova.on_message(ALAKH)
async def handle_incoming(_, message):
    results = await handle_alakh(message.text)
    await message.reply(results)
