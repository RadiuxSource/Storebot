from zenova import zenova, BOT_ID
import requests, json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.database import present_group, add_group, unpresent_quizzez, add_quizzez, del_quizzez, full_quizzezbase, full_groupbase
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import PollType
from config import DB_URI
from config2 import LOGGER_ID
from helper_func import is_admin
from helper.prompts import quiz_ai
from pyrogram import filters
from pyrogram.types import ChatMemberUpdated

API_URL = "https://chatgpt.apinepdev.workers.dev/?question="
scheduler = AsyncIOScheduler()


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


@zenova.on_message(filters.command(['quiz'], prefixes='/'))
async def quiz_mode(client, message: Message):
    chat_id = message.chat.id
    msg_id = message.id
    # if group type is not group
    if message.chat.type != 'GROUP' or message.chat.type != 'SUPERGROUP':
        await message.reply('🚫 This command can only be used in groups.', reply_to_message_id=msg_id)
        return
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
    response = requests.get(f"{API_URL}{await quiz_ai()}")
    result = response.json()
    question = result.get("answer", "No answer received from ChatGPT.")
    return question

async def send_quiz():
    groups = await full_groupbase()
    quizzez_chats = await full_quizzezbase()
    for chat_id in groups:
        if chat_id not in quizzez_chats:
            try:
                question = await get_question()
                options = question["options"]
                correct_option_id = question["correct_option_id"]
                poll = await zenova.send_poll(chat_id, question["question"], options, is_anonymous= False, type=PollType.QUIZ, correct_option_id= correct_option_id, explanation= 'Note: AI-generated quiz. Verify answers independently.',)
            except Exception as e:
                print(f"Error sending quiz to chat {chat_id}: {e}")

scheduler.add_job(send_quiz, 'interval', minutes=10)
scheduler.start()