from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from zenova import zenova
from config2 import LOGGER_ID, STORE_ID, QR_CODE
from config import ADMINS
import pyrostep
import os

pyrostep.listen(zenova)
shop_list = []

@zenova.on_message(filters.command("add") & filters.user(ADMINS))
async def add_to_shop(client, message: Message):
    await message.reply_text("Enter the message to add to the shop: 🛍️")
    msg: Message = await pyrostep.wait_for(message.from_user.id)
    sent_msg: Message = await zenova.copy_message(STORE_ID, msg.chat.id, msg.id)
    shop_list.append(sent_msg.id)
    await message.reply_text("Message added to the shop successfully! 👍")

@zenova.on_message(filters.command("list") & filters.user(ADMINS))
async def list_shop(client, message: Message):
    if not shop_list:
        await message.reply_text("The shop is empty! 😔")
        return
    text = "List of all the messages in the shop:\n\n"
    for i, msg_id in enumerate(shop_list.copy()):
        text += f"{i+1}. {msg_id}\n"
    await message.reply_text(text)

#function to delete a id
@zenova.on_message(filters.command("del") & filters.user(ADMINS))
async def delete_from_shop(client, message: Message):
    if not shop_list:
        await message.reply_text("The shop is empty! 😔")
        return
    await message.reply_text("Enter the message ID to delete from the shop: 🛍️")
    msg: Message = await pyrostep.wait_for(message.from_user.id)
    if msg.text:
        shop_list.remove(msg.text)
        await message.reply_text("Message deleted from the shop successfully! 👍")
    else:
        await message.reply_text("Invalid message ID. Please enter a valid message ID.")

@zenova.on_message(filters.command("shop"))
async def shop(client, message):
    try:
        if not shop_list:
            await message.reply_text("The shop is empty! 😔")
            return
        current_msg_id = shop_list[0]
        await send_shop_message(message, current_msg_id, 0)
    except Exception as e:
        await message.reply_text("Error: Unable to retrieve shop list. 😕")
        print(f"Error: {e}")

async def send_shop_message(message: Message, msg_id, index):
    try:
        msg = await zenova.get_messages(STORE_ID, msg_id)
        keyboard = []
        if len(shop_list) > 1:
            keyboard.append([
                InlineKeyboardButton("Prev 🔙" if index > 0 else "Prev 🔙 (No more)", callback_data=f"Sprev_{index}"),
                InlineKeyboardButton("Next 🔜" if index < len(shop_list) - 1 else "Next 🔜 (No more)", callback_data=f"Snext_{index}")
            ])
        keyboard.append([InlineKeyboardButton("Buy Now 💸", callback_data=f"buy_{index}")])
        if msg.media:
            photo_file = await zenova.download_media(message=msg, file_name=f'photo_{message.from_user.id}.jpg')
            await message.reply_photo(photo_file, msg.text, reply_markup=InlineKeyboardMarkup(keyboard))
            os.remove(path=photo_file)
        else:
            await message.reply_text(msg.text, reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as e:
        await message.reply_text("Error: Unable to retrieve shop message. 😕")
        print(f"Error: {e}")

@zenova.on_callback_query(filters.regex(r"Sprev|Snext|buy"))
async def shop_callback(client, callback_query: CallbackQuery):
    try:
        data: str = callback_query.data
        id = callback_query.from_user.id
        if data.startswith("Sprev"):
            index = int(data.split("_")[1])
            new_index = (index - 1) % len(shop_list)
            new_msg_id = shop_list[new_index]
            new_msg: Message = await zenova.get_messages(STORE_ID, new_msg_id)
            if new_msg.media:
                photo_file = await zenova.download_media(message=new_msg, file_name=f'photo_{id}.jpg')
                await callback_query.message.edit_media(photo_file)
                os.remove(path=photo_file)
            await callback_query.message.edit_text(new_msg.text, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Buy Now 💸", callback_data=f"buy_{new_index}")],
                [InlineKeyboardButton("Prev 🔙" if new_index > 0 else "Prev 🔙 (No more)", callback_data=f"Sprev_{new_index}"),
                 InlineKeyboardButton("Next 🔜" if new_index < len(shop_list) - 1 else "Next 🔜 (No more)", callback_data=f"Snext_{new_index}")]
            ]))
        elif data.startswith("Snext"):
            index = int(data.split("_")[1])
            new_index = (index + 1) % len(shop_list)
            new_msg_id = shop_list[new_index]
            new_msg: Message = await zenova.get_messages(STORE_ID, new_msg_id)
            if new_msg.media:
                photo_file = await zenova.download_media(message=new_msg, file_name=f'photo_{id}.jpg')
                await callback_query.message.edit_media(photo_file)
                os.remove(path=photo_file)
            await callback_query.message.edit_text(new_msg.text, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Buy Now 💸", callback_data=f"buy_{new_index}")],
                [InlineKeyboardButton("Prev 🔙" if new_index > 0 else "Prev 🔙 (No more)", callback_data=f"Sprev_{new_index}"),
                 InlineKeyboardButton("Next 🔜" if new_index < len(shop_list) - 1 else "Next 🔜 (No more)", callback_data=f"Snext_{new_index}")]
            ]))
        elif data.startswith("buy"):
            index = int(data.split("_")[1])
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Yes 👍", callback_data=f"yes_{index}"), 
                 InlineKeyboardButton("No 👎", callback_data=f"no_{index}")]
            ])
            await callback_query.message.edit_text("Are you sure you want to buy this? 🤔", reply_markup=keyboard)
    except Exception as e:
        await callback_query.message.reply_text("Error: Unable to process query. 😕")
        print(f"Error: {e}")

@zenova.on_callback_query(filters.regex(r"yes|no"))
async def buy_callback(client, callback_query: CallbackQuery):
    data = callback_query.data
    if data.startswith("yes"):
        index = int(data.split("_")[1])
        msg_id = shop_list[index]
        msg = await client.get_messages(STORE_ID, msg_id)
        await callback_query.message.reply_photo(QR_CODE, "Pay on this QR code 💳 and send the screenshot of payment and wait for confirmation, You can also DM to my owner to know the status: @Haaye_Aman")
        await client.send_message(LOGGER_ID, f"New Order 📝\n\nPurchaser: {callback_query.from_user.id}", reply_to_message_id=msg_id)
        await callback_query.message.delete()
    elif data.startswith("no"):
        await callback_query.message.edit_text("Order cancelled! 😔")