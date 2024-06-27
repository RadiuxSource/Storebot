import re

from pyrogram import filters, enums
from zenova import zenova 
from db import add_user, present_user
import config2 as config
from helper.messages import (
    START_TXT, 
    NOTICE_TXT, 
    START_BTN,
    CMD_LIST,
    HELP_MSG,
    HELP_MARKUP,
    CMD_MARKUP,
)



@zenova.on_message((filters.command(["start"]))) 
async def start(client, message):
    id = message.from_user.id
    present, count = await present_user(id)
    if not present:
        try:
            await add_user(id)
            INFO = f'''
#NewUser

Total users = [{int(count) + 1}]
User id = {id}
Link = {message.from_user.mention()}
'''
            await client.send_message(config.LOGGER_ID, INFO)
        except:
            pass
    await message.reply(NOTICE_TXT)
    await message.reply_photo(config.Start_img, caption= START_TXT, reply_markup=START_BTN)


@zenova.on_message(filters.command("help"))
async def help_command(client, message):
    id = message.from_user.id
    present, count = await present_user(id)
    if not present:
        try:
            await add_user(id)
            INFO = f'''
#NewUser

Total users = [{int(count) + 1}]
User id = {id}
Link = {message.from_user.mention()}
'''
            await client.send_message(config.LOGGER_ID, INFO)
        except:
            pass
    await message.reply_text(HELP_MSG, reply_markup=HELP_MARKUP)
   
@zenova.on_callback_query(filters.regex(re.compile('home|commands|help_back')))
async def start_query(_, query):
    if query.data == "home":
        await query.message.edit_caption(START_TXT, reply_markup=START_BTN)
    elif query.data == "commands":
        await query.message.edit_text(CMD_LIST, parse_mode=enums.ParseMode.MARKDOWN, reply_markup=CMD_MARKUP)
    elif query.data == "help_back":    
         await query.message.edit_text(HELP_MSG, reply_markup=HELP_MARKUP)
