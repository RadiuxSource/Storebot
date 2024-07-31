# External libraries
import requests
import json
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatMemberUpdated
from pyrogram.errors import FloodWait, InputUserDeactivated, PeerIdInvalid, ChatWriteForbidden, MessageTooLong
from pyrogram.enums import PollType

# Local modules
from zenova import zenova, BOT_ID
from database.database import present_group, add_group, unpresent_quizzez, add_quizzez, del_quizzez, full_quizzezbase, full_groupbase
from config import DB_URI
from config2 import LOGGER_ID
from helper_func import is_admin
from helper.prompts import quiz_ai
from helper.blackbox import Blackbox

# API URL
API_URL = "https://chatgpt.apinepdev.workers.dev/?question="

# Scheduler
scheduler = AsyncIOScheduler()

# Failed chats list
failed_chats = []


@zenova.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    if not user.id == BOT_ID:
        return
    chat_id = member.chat.id
    present, count = await present_group(chat_id)
    if not present:
        try:
            await add_group(chat_id)
            INFO = f'''
#NewChat

Total chats = [{int(count) + 1}]
Chat id = {chat_id}
Name = {member.chat.title}
'''
            await zenova.send_message(LOGGER_ID, INFO)
        except:
            pass


@zenova.on_message(filters.command('quiz') & filters.group)
async def quiz_mode(client, message: Message):
    chat_id = message.chat.id
    present, count = await present_group(chat_id)
    if not present:
        try:
            await add_group(chat_id)
            INFO = f'''
#NewChat

Total chats = [{int(count) + 1}]
Chat id = {chat_id}
Name = {message.chat.title}
'''
            await zenova.send_message(LOGGER_ID, INFO)
        except:
            pass
    msg_id = message.id
    # # if group type is not group
    # if message.chat.type != 'GROUP' or message.chat.type != 'SUPERGROUP':
    #     await message.reply('🚫 This command can only be used in groups.', reply_to_message_id=msg_id)
    #     return
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.reply('🚫 You don\'t have access to this command.', reply_to_message_id=msg_id)
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply('🚫 Wrong usage. Use /quiz on/off', reply_to_message_id=msg_id)
        return
    mode = args[1]
    if mode not in ['on', 'off']:
        await message.reply('🚫 Wrong usage. Use /quiz on/off', reply_to_message_id=msg_id)
        return
    unpresent = await unpresent_quizzez(chat_id)
    if mode == 'on':
        if not unpresent:
            await message.reply('🚫 Quiz mode is already on in this chat.', reply_to_message_id=msg_id)
            return
        await del_quizzez(chat_id)
        await message.reply('🟢 Quiz mode is now on in this chat.', reply_to_message_id=msg_id)
    else:
        if unpresent:
            await message.reply('🚫 Quiz mode is already off in this chat.', reply_to_message_id=msg_id)
            return
        await add_quizzez(chat_id)
        await message.reply('🔴 Quiz mode is now off in this chat.', reply_to_message_id=msg_id)


async def get_question():
    blackbox = Blackbox()
    sys_prompt, subject = await quiz_ai()
    content = f"Generate a question for the {subject} subject."
    response = blackbox.request(content, sys_prompt)
    # response = requests.get(f"{API_URL}{await quiz_ai()}")
    result = response.json()
    question = result.get("answer", "No answer received from ChatGPT.")
    return question

async def send_quiz():
    groups = await full_groupbase()
    quizzez_chats = await full_quizzezbase()
    for chat_id in groups:
        if chat_id not in quizzez_chats:
            await send_polls(int(chat_id))
            
async def send_polls(chat_id: int):
    try:
        question = await get_question()
        question = json.loads(question)
        options = question["options"]
        correct_option_id = question["correct_option_id"]
        poll = await zenova.send_poll(int(chat_id), question["question"], options, is_anonymous= False, type=PollType.QUIZ, correct_option_id= int(correct_option_id), explanation= 'Note: AI-generated quiz. Verify answers independently.',)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_polls(chat_id)
    except InputUserDeactivated:
        print(f"{chat_id} : Deactivated")
        failed_chats.append(chat_id)
        return 400
    except PeerIdInvalid:
        print(f"{chat_id} : PeerIdInvalid")
        failed_chats.append(chat_id)
        return 400
    except ChatWriteForbidden:
        print(f"{chat_id} : Invalid ID")
        failed_chats.append(chat_id)
        return 400
    except MessageTooLong:
        print(f"{chat_id} : Message too long")
        return await send_polls(chat_id)
    except Exception as e:
        print(f"Error sending quiz to chat {chat_id}: {e}")
        return 500
            

scheduler.add_job(send_quiz, 'interval', minutes=30)
scheduler.start()