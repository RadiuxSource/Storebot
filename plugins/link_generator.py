#(©)Codexbotz

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id
import json

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except Exception as e:
            print("An error occured while batching:", e)
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue

    while True:
        try:
            second_message = await client.ask(text = "Forward the Last Message from DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue


    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "Forward Message from the DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is not taken from DB Channel", quote = True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch_poll'))
async def batch_poll(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text="Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link", chat_id=message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply(" Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote=True)
            continue

    while True:
        try:
            second_message = await client.ask(text="Forward the Last Message from DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id=message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply(" Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote=True)
            continue

    message_ids = list(range(f_msg_id, s_msg_id + 1))
    questions = []
    for msg_id in message_ids:
        try:
            msg = await client.get_messages(chat_id=client.db_channel.id, message_ids=msg_id)
            if msg.photo:
                # Get the photo link
                photo_link = await upload_photo(msg.photo.file_id)
                # Get the next poll message
                next_msg_id = msg_id + 1
                while True:
                    try:
                        next_msg = await client.get_messages(chat_id=client.db_channel.id, message_ids=next_msg_id)
                        if next_msg.poll:
                            break
                        next_msg_id += 1
                    except:
                        next_msg_id += 1
                        continue
                if next_msg.poll:
                    # Fetch poll details
                    poll_details = {
                        "question": next_msg.poll.question,
                        "options": next_msg.poll.options,
                        "correct_option_id": next_msg.poll.correct_option_id,
                        "image": photo_link
                    }
                    questions.append(poll_details)
            elif msg.poll:
                # Fetch poll details
                poll_details = {
                    "question": msg.poll.question,
                    "options": msg.poll.options,
                    "correct_option_id": msg.poll.correct_option_id,
                    "image": None
                }
                questions.append(poll_details)
        except:
            continue

    # Create a JSON file with the questions
    with open('questions.json', 'w') as f:
        json.dump(questions, f, indent=4)

    # Send the JSON file to the admin
    with open('questions.json', 'rb') as f:
        await client.send_document(chat_id=message.from_user.id, document=f, file_name='questions.json')