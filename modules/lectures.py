#(©)Zenova_Lectures_Bot

import logging
import base64
import random
import re
import string
import time
import asyncio
from datetime import datetime, timedelta
import requests

from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, ButtonDataInvalid, MessageNotModified

from zenova import zenova as Bot
from db import add_user, present_user, update_verification, check_verification
import config2 as config
from config2 import LOGGER_ID, IS_VERIFY, VERIFY_EXPIRE, SHORTLINK_URL, SHORTLINK_API, VERIFY_TUT_VID

# Helper functions
async def generate_verify_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def get_exp_time(seconds):
    hours = seconds // 3600
    return f"{hours} hours"

async def get_shortlink(url, api, link):
    try:
        shortzy = Shortzy(api, url)
        return await shortzy.convert(link)
    except Exception as e:
        logging.error(f"Shortlink error: {e}")
        return link  # Fallback to original link if shortener fails

# Messages and buttons (keep existing)
strt_txt = '''👋 **Wᴇʟᴄᴏᴍᴇ ᴛᴏ Zᴇɴᴏᴠᴀ Lᴇᴄᴛᴜʀᴇs Bᴏᴛ!**

Get ready for an enriching learning experience with free lectures from various teachers!'''
# ... [keep all your existing message texts and button configurations] ...

# Verification handler
@Bot.on_message(filters.command('start') & filters.private & filters.regex(r'^verify_'))
async def verify_handler(client, message):
    id = message.from_user.id
    token = message.text.split('_')[1]
    
    verify_status = await check_verification(id)
    
    if not verify_status or verify_status.get('verify_token') != token:
        return await message.reply("❌ Invalid or expired verification token. Please try again.")
    
    await update_verification(id, is_verified=True, verified_time=time.time())
    
    await message.reply(
        f"✅ Verification Successful!\n\n"
        f"⏳ You now have access for: {get_exp_time(VERIFY_EXPIRE)}\n\n"
        f"Use /lecture to browse available lectures.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📚 Browse Lectures", callback_data="lecture_start")]
        ])
    )

# Modified start command
@Bot.on_message(filters.command(["start"]))
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
            await client.send_message(LOGGER_ID, INFO)
        except:
            pass
    
    if "verify_" in message.text:
        return await verify_handler(client, message)
    
    await message.reply(Notice_txt)
    await message.reply_photo(config.Start_img, caption=strt_txt, reply_markup=strt_btn)

# Modified lectures command with verification
@Bot.on_message(filters.command('lecture') & filters.private)
async def lectures_command(client, message):
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
            await client.send_message(LOGGER_ID, INFO)
        except:
            pass
    
    # Verification check
    if IS_VERIFY:
        verify_status = await check_verification(id)
        
        if verify_status['is_verified'] and verify_status['verified_time']:
            elapsed = time.time() - verify_status['verified_time']
            if elapsed > VERIFY_EXPIRE:
                await update_verification(id, is_verified=False)
                verify_status['is_verified'] = False
        
        if not verify_status['is_verified']:
            token = await generate_verify_token()
            await update_verification(id, is_verified=False, token=token)
            
            try:
                verify_link = await get_shortlink(
                    SHORTLINK_URL,
                    SHORTLINK_API,
                    f'https://t.me/{client.username}?start=verify_{token}'
                )
            except Exception as e:
                logging.error(f"Shortlink error: {e}")
                return await message.reply("⚠️ Verification service temporarily unavailable. Please try again later.")
            
            btn = [
                [InlineKeyboardButton("🔗 Verify Now", url=verify_link)],
                [InlineKeyboardButton("📺 How to Verify", url=VERIFY_TUT_VID)]
            ]
            
            return await message.reply(
                f"🔒 Verification Required\n\n"
                f"To access lectures, please complete verification first.\n\n"
                f"⏳ After verification, you'll have access for: {get_exp_time(VERIFY_EXPIRE)}\n\n"
                f"📌 This helps prevent abuse and maintain service quality.",
                reply_markup=InlineKeyboardMarkup(btn),
                protect_content=False
            )
    
    # Original lectures functionality
    reply_markup = InlineKeyboardMarkup(gpay)
    await message.reply_text("𝐂𝙷𝙾𝚂𝙴 𝙰 𝐒𝚄𝙱𝙹𝙴𝙲𝚃 𝐅𝚁𝙾𝙼 𝐁𝙴𝙻𝙾𝚆 𝐏𝙻𝙴𝙰𝚂𝙴 :", reply_markup=reply_markup)

# ... [keep all your existing callback handlers and other functions] ...

@Bot.on_callback_query()
async def handle_callback(_, query):
    if query.data.startswith("subject_"):
        # Add verification check for subject selection
        if IS_VERIFY:
            verify_status = await check_verification(query.from_user.id)
            if not verify_status.get('is_verified', False):
                await query.answer("Please complete verification first using /lecture", show_alert=True)
                return
        
        subject = query.data.split("_")[1]
        response = requests.get(f"https://zenova-api-green.vercel.app/teachers?subject={subject}")
        if response.status_code == 200:
            teachers_data = response.json()
            teachers = teachers_data.get("teachers", [])
            buttons = []
            row = []
            for teacher in teachers:
                row.append(InlineKeyboardButton(teacher, callback_data=f"teacher_{subject}_{teacher}"))
                if len(row) == 2:
                    buttons.append(row)
                    row = []
            if row:
                buttons.append(row)
            buttons.append([InlineKeyboardButton("×͜× SUBJECTS ×͜×", callback_data="subject")])
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(f"𝐂𝙷𝙾𝚂𝙴 𝙰 𝐓𝙴𝙰𝙲𝙷𝙴𝚁 𝐅𝙾𝚁 {subject}:", reply_markup=reply_markup)
        else:
            await message.reply_text(f"Failed to fetch chapters. Please try again later. Exception: {c}")
        return

    # Send the chapters for the next page
    await send_chapters_pages(message, chapters, subject, teacher_name, next_page)

async def send_chapters_pages(message, chapters, subject, teacher_name, current_page, previous_page=None, next_page=None):
    # Calculate the total number of pages
    chapters_per_page = 7
    total_pages = (len(chapters) + chapters_per_page - 1) // chapters_per_page

    # If the current page is not provided, calculate it from the previous or next page
    if current_page is None:
        if previous_page is not None:
            current_page = previous_page
        elif next_page is not None:
            current_page = next_page
        else:
            current_page = 1

    # Calculate the start and end index of chapters for the current page
    start_index = (current_page - 1) * chapters_per_page
    end_index = min(start_index + chapters_per_page, len(chapters))

    # Create rows with two buttons each for chapters
    buttons = []
    row = []
    for chapter in chapters[start_index:end_index]:
        row.append(InlineKeyboardButton(chapter, callback_data=f"chapter_{subject}_{teacher_name}_{chapter}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    # Add pagination buttons
    pagination_buttons = []
    if current_page > 1:
        print(f"current page: {current_page}")
        pagination_buttons.append(InlineKeyboardButton(" ☚", callback_data=f"prev_page_{subject}_{teacher_name}_{current_page - 1}"))
    if current_page == 1:
        xytra = total_pages
        pagination_buttons.append(InlineKeyboardButton(" ☚", callback_data=f"prev_page_{subject}_{teacher_name}_{xytra}"))
    pagination_buttons.append(InlineKeyboardButton("߷ 𝐓ᴇᴀᴄʜᴇʀs ߷",  callback_data=f"subject_{subject}"))
    if current_page < total_pages:
        pagination_buttons.append(InlineKeyboardButton("☛", callback_data=f"next_page_{subject}_{teacher_name}_{current_page + 1}"))
    if current_page == total_pages:
        radiux = 1
        pagination_buttons.append(InlineKeyboardButton("☛", callback_data=f"next_page_{subject}_{teacher_name}_{radiux}"))
    buttons.append(pagination_buttons)
    
    try:
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.edit_text(f"Page {current_page}/{total_pages} - Please choose a chapter from below buttons:", reply_markup=reply_markup)
    except ButtonDataInvalid as bd:
        await message.reply_text(f"InlineButton text too long.\n\n Please report it to support chat")
    except MessageNotModified as mn:
        await message.reply_text("Their is no other pages!!")
    except rpc_error as chut:
        await message.reply_text(f"An error occured: {chut}\n\n Please report it to support chat!!")


@Bot.on_message(filters.command('lecture') & filters.group)
async def lectures_command(client, message):
    BOT_USERNAME = config.BOT_USERNAME
    markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("𝐔ᴘᴅᴀᴛᴇs", url=config.UPDATE),
    InlineKeyboardButton("𝐒ᴜᴘᴘᴏʀᴛ", url=config.SUPPORT)],
    [InlineKeyboardButton("𝐔sᴇ ᴍᴇ ɪɴ ᴘᴍ", url=f"t.me/{BOT_USERNAME}?start")]    
    ]) 
    # Send the message with the inline keyboard
    await message.reply_text("𝐈 𝐂𝙰𝙽 𝐎𝙽𝙻𝚈 𝐁𝙴 𝐔𝚂𝙴𝙳 𝐈𝙽 𝐓𝙷𝙴 𝐏𝚁𝙸𝚅𝙰𝚃𝙴 𝐌𝙾𝙳𝙴 !!", reply_markup=markup)
