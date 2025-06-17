#(©)Codeflix_Bots

import logging
import base64
import random
import re
import string
import time
import asyncio

from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import (
    ADMINS,
    FORCE_MSG,
    START_MSG,
    CUSTOM_CAPTION,
    IS_VERIFY,
    VERIFY_EXPIRE,
    SHORTLINK_API,
    SHORTLINK_URL,
    DISABLE_CHANNEL_BUTTON,
    PROTECT_CONTENT,
    TUT_VID,
    OWNER_ID,
)
from helper_func import subscribed, encode, decode, get_messages, get_shortlink, get_verify_status, update_verify_status, get_exp_time
from database.database import add_user, del_user, full_userbase, present_user
from shortzy import Shortzy

# Verification expiry set to 36 hours (129600 seconds)
VERIFICATION_EXPIRE_TIME = 129600

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    
    # Owner bypass
    if id == OWNER_ID:
        await message.reply("🛠️ Owner Mode Activated! What would you like to do today?")
        return

    # Add new user to database
    if not await present_user(id):
        try:
            await add_user(id)
        except Exception as e:
            logging.error(f"Error adding user {id}: {e}")

    verify_status = await get_verify_status(id)
    
    # Check if verification expired
    if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
        await update_verify_status(id, is_verified=False)
        verify_status['is_verified'] = False

    # Handle verification token
    if "verify_" in message.text:
        _, token = message.text.split("_", 1)
        if verify_status['verify_token'] != token:
            return await message.reply("❌ Invalid or expired token. Please try again with /start")
        
        await update_verify_status(id, is_verified=True, verified_time=time.time())
        remaining_time = get_exp_time(VERIFY_EXPIRE)
        await message.reply(
            f"✅ Verification Successful!\n\n"
            f"⏳ Access granted for: {remaining_time}\n\n"
            f"Enjoy using the bot!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🏠 Main Menu", callback_data="start")]]
            ),
            protect_content=False
        )
        return

    # Content access for verified users
    elif len(message.text) > 7 and verify_status['is_verified']:
        try:
            base64_string = message.text.split(" ", 1)[1]
        except:
            return await message.reply("⚠️ Invalid request format")
        
        try:
            _string = await decode(base64_string)
            argument = _string.split("-")
            
            if len(argument) == 3:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end+1) if start <= end else list(reversed(range(end, start+1)))
            elif len(argument) == 2:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            else:
                return await message.reply("⚠️ Invalid request format")
        except:
            return await message.reply("⚠️ Invalid request format")

        temp_msg = await message.reply("⏳ Processing your request...")
        
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            logging.error(f"Error getting messages: {e}")
            return await temp_msg.edit("❌ Failed to process your request")

        await temp_msg.delete()
        snt_msgs = []
        
        for msg in messages:
            caption = CUSTOM_CAPTION.format(
                previouscaption="" if not msg.caption else msg.caption.html,
                filename=msg.document.file_name if msg.document else ""
            ) if CUSTOM_CAPTION and msg.document else ("" if not msg.caption else msg.caption.html)

            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

            try:
                snt_msg = await msg.copy(
                    chat_id=id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                await asyncio.sleep(0.5)
                snt_msgs.append(snt_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                snt_msg = await msg.copy(
                    chat_id=id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                snt_msgs.append(snt_msg)
            except Exception as e:
                logging.error(f"Error sending message: {e}")

        warning = await message.reply("⚠️ Files will auto-delete in 10 minutes. Save them now!")
        await asyncio.sleep(600)
        
        for snt_msg in snt_msgs:
            try:
                await snt_msg.delete()
            except:
                pass
        try:
            await warning.delete()
        except:
            pass

    # Verified user menu
    elif verify_status['is_verified']:
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=f"@{message.from_user.username}" if message.from_user.username else "N/A",
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ℹ️ About", callback_data="about"),
                 InlineKeyboardButton("❌ Close", callback_data="close")]
            ]),
            disable_web_page_preview=True
        )

    # Verification required
    else:
        if IS_VERIFY:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            await update_verify_status(id, verify_token=token, link="")
            
            try:
                verification_link = await get_shortlink(
                    SHORTLINK_URL,
                    SHORTLINK_API,
                    f'https://telegram.dog/{client.username}?start=verify_{token}'
                )
            except Exception as e:
                logging.error(f"Shortlink error: {e}")
                return await message.reply("⚠️ Verification service temporarily unavailable. Please try again later.")

            await message.reply(
                f"🔒 Verification Required\n\n"
                f"To prevent abuse, please complete verification:\n\n"
                f"1. Click 'Verify Now' below\n"
                f"2. Complete the quick process\n"
                f"3. Get {get_exp_time(VERIFY_EXPIRE)} of access\n\n"
                f"Need help? Watch our tutorial!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔗 Verify Now", url=verification_link)],
                    [InlineKeyboardButton("📺 Tutorial Video", url=TUT_VID)]
                ]),
                protect_content=False
            )

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton("📢 Join Channel 1", url=client.invitelink),
            InlineKeyboardButton("📢 Join Channel 2", url=client.invitelink2)
        ],
        [
            InlineKeyboardButton("📢 Join Channel 3", url=client.invitelink3)
        ]
    ]
    
    try:
        buttons.append([
            InlineKeyboardButton(
                "🔄 Try Again",
                url=f"https://t.me/{client.username}?start={message.command[1]}"
            )
        ])
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=f"@{message.from_user.username}" if message.from_user.username else "N/A",
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await message.reply("📊 Getting user statistics...")
    users = await full_userbase()
    await msg.edit(f"👥 Total Users: {len(users)}")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def broadcast_handler(client: Bot, message: Message):
    if not message.reply_to_message:
        return await message.reply("ℹ️ Please reply to a message to broadcast")
    
    users = await full_userbase()
    broadcast_msg = message.reply_to_message
    total = len(users)
    successful = blocked = deleted = unsuccessful = 0
    
    progress = await message.reply(f"📢 Broadcasting to {total} users...\n\n"
                                 f"✅ Successful: 0\n"
                                 f"🚫 Blocked: 0\n"
                                 f"💀 Deleted: 0\n"
                                 f"❌ Failed: 0")
    
    for user_id in users:
        try:
            await broadcast_msg.copy(user_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await broadcast_msg.copy(user_id)
            successful += 1
        except UserIsBlocked:
            await del_user(user_id)
            blocked += 1
        except InputUserDeactivated:
            await del_user(user_id)
            deleted += 1
        except Exception as e:
            unsuccessful += 1
            logging.error(f"Broadcast error for {user_id}: {e}")
        
        if (successful + blocked + deleted + unsuccessful) % 10 == 0:
            await progress.edit(f"📢 Broadcasting to {total} users...\n\n"
                              f"✅ Successful: {successful}\n"
                              f"🚫 Blocked: {blocked}\n"
                              f"💀 Deleted: {deleted}\n"
                              f"❌ Failed: {unsuccessful}")
    
    await progress.edit(
        f"📊 Broadcast Complete!\n\n"
        f"👥 Total Users: {total}\n"
        f"✅ Successful: {successful}\n"
        f"🚫 Blocked: {blocked}\n"
        f"💀 Deleted: {deleted}\n"
        f"❌ Failed: {unsuccessful}"
    )
