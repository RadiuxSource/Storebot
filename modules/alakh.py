from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from youtubesearchpython import CustomSearch, SearchMode

import aiohttp
from helper.prompts import alakh_ai, search_ai
from zenova import zenova
import json
import requests

API_URL = "https://chatgpt.apinepdev.workers.dev/?question="
YT_SEARCH_API = "https://chat-gpt.hazex.workers.dev/"  

async def handle_alakh(message, title = None):
    txt = message
    async with aiohttp.ClientSession() as session:
        if title:
             async with session.get(f"{API_URL}'prompt' :{alakh_ai}, 'title': {title}, 'user':{txt}") as response:
                 data = await response.text()
        else:
            async with session.get(f"{API_URL}'prompt' :{alakh_ai},'title': None, 'user':{txt}") as response:
                data = await response.text()
        answer = json.loads(data)['answer']
        return answer


async def search_ai(message: str):
    data = {"user": search_ai + "user:" + message}
    response = requests.post(YT_SEARCH_API, json=data)
    response_json = response.json()
    answer = json.loads(response_json['answer'])
    if answer['relevant']:
        query = answer['search_query']
        video_url =await search_youtube(query)
        return video_url, answer['title']
    return None, None

async def search_youtube(search_query: str):
    custom_search = CustomSearch(search_query, searchPreferences=SearchMode.videos, language='hi', region='In')
    results = custom_search.result()['result']
    if not results:
        return None
    video_url = results[0]['link']
    return video_url

async def is_alakh(_, __, update: Message):
    if not update.text: return False
    return any(word in update.text.lower() for word in ['alakh'])

ALAKH = filters.create(is_alakh)

@zenova.on_message(ALAKH)
async def handle_incoming(_, message: Message):
    video_url, title = await search_youtube(message.text)
    if video_url:
        results = await handle_alakh(message.text, title = title)
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(title, url=video_url)]
        ])
        await message.reply(results, reply_markup=markup)
    else:
        results = await handle_alakh(message.text)
        await message.reply(results)