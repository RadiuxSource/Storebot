from pyrogram import filters, Client
import json, asyncio

from telegraph import upload_file, TelegraphException
from telegraph.exceptions import RetryAfterError

from zenova import zenova
from config import ADMINS, POLL_DB
from helper_func import get_message_id


async def upload_photo(message, path):
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            link = upload_file(path)
            generated_link = "https://telegra.ph" + "".join(link)
            return generated_link
        except RetryAfterError as e:
            await message.reply(f"Flood control exceeded. Retrying after {e.retry_after} seconds")
            await asyncio.sleep(e.retry_after)
            retries += 1
        except TelegraphException as e:
            await message.reply(f"Error uploading image: {e}")
            return None
        except Exception as e:
            await message.reply(f"Error uploading image: {e}")
            return None
    await message.reply("Maximum retries exceeded, giving up")
    return None


@zenova.on_message(filters.private & filters.user(ADMINS) & filters.command('batch_poll'))
async def batch_poll(client: Client, message):
    while True:
        try:
            first_message = await client.ask(text="Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link", chat_id=message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message, poll= True)
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
        s_msg_id = await get_message_id(client, second_message, poll= True)
        if s_msg_id:
            break
        else:
            await second_message.reply(" Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote=True)
            continue

    message_ids = list(range(f_msg_id, s_msg_id + 1))
    questions = []
    for msg_id in message_ids:
        try:
            msg = await client.get_messages(chat_id=POLL_DB, message_ids=msg_id)
            if msg.photo:
                photo_path = await client.download_media(message=msg, file_name=f"image/photo{msg_id}.jpg")
                # Get the photo link
                photo_link = await upload_photo(message, photo_path)
                # Get the next poll message
                next_msg_id = msg_id + 1
                while True:
                    try:
                        next_msg = await client.get_messages(chat_id=POLL_DB, message_ids=next_msg_id)
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