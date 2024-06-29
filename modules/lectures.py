import re

from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import ButtonDataInvalid, MessageNotModified, rpc_error

from zenova import zenova as Bot
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
    SUBJECTS_BTN
)

from helper.request import get_teachers, get_chapters, get_lecture_link



@Bot.on_message(filters.command('lecture'))
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
            await client.send_message(config.LOGGER_ID, INFO)
        except:
            pass
    # Create the InlineKeyboardMarkup object
    reply_markup = InlineKeyboardMarkup(SUBJECTS_BTN)
    # Send the message with the inline keyboard
    await message.reply_text("━━━━━━━━━━━━━━━━━━━━━━\n\n𝙲𝙷𝙾𝙾𝚂𝙴 𝙰 𝚂𝚄𝙱𝙹𝙴𝙲𝚃 𝙵𝚁𝙾𝙼 𝙱𝙴𝙻𝙾𝚆 𝙿𝙻𝙴𝙰𝚂𝙴 🥀 :", reply_markup=reply_markup)

@Bot.on_callback_query(filters.regex(re.compile('subject_|subject|teacher_|chapter_|prev_page_|next_page_')))
async def handle_callback(_, query):
    if query.data.startswith("subject_"):
        subject = query.data.split("_")[1]
        teachers_data = await get_teachers(subject)
        if teachers_data:
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
            buttons.append([InlineKeyboardButton("✾ 𝚂𝚄𝙱𝙹𝙴𝙲𝚃𝚂 ✾", callback_data="subject")])
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(f"╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺\n\n**Select a Teacher for {subject} :** 💐", reply_markup=reply_markup)
        else:
            await query.message.edit_text("Failed to fetch data from the API. Please try again later.")
    elif query.data == "subject":
        reply_markup = InlineKeyboardMarkup(SUBJECTS_BTN)
        await query.message.edit_text("━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n𝙲𝙷𝙾𝙾𝚂𝙴 𝙰 𝚂𝚄𝙱𝙹𝙴𝙲𝚃 𝚃𝙾 𝙿𝚁𝙾𝙲𝙴𝙴𝙳 🦋 :", reply_markup = reply_markup)
    elif query.data.startswith("teacher_"):
        data_parts = query.data.split("_")
        subject = data_parts[1]
        teacher_name = data_parts[2]
        try:
            chapters_data = await get_chapters(subject, teacher_name)
            if chapters_data:
                chapters = chapters_data.get("chapters", [])
                current_page = 1
                next_page = 2
                await send_chapters_pages(query.message, chapters, subject, teacher_name, current_page, next_page, query)
            else:
                await query.message.edit_text("𝙵𝙰𝙸𝙻𝙴𝙳 𝚃𝙾 𝙵𝙴𝚃𝙲𝙷 𝙳𝙰𝚃𝙰 𝙵𝚁𝙾𝙼 𝙰𝙿𝙸, 𝙿𝙻𝙴𝙰𝚂𝙴 𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽 𝙻𝙰𝚃𝙴𝚁.")
        except ButtonDataInvalid as bd:
            print('ButtonDataInvalid:', bd)
        except Exception as e:
            print('Exception:', e)
    elif query.data.startswith("chapter_"):
        data_parts = query.data.split("_")
        subject = data_parts[1]
        teacher_name = data_parts[2]
        chapter_name = data_parts[3]
        lecture_link = await get_lecture_link(subject, teacher_name, chapter_name)
        if lecture_link:
            shivabeta = [
                        [
                            InlineKeyboardButton("❈ 𝐋ᴇᴄᴛᴜʀᴇs ❈", url= lecture_link),
                            InlineKeyboardButton("❈ 𝐁ᴀᴄᴋ ❈", f"teacher_{subject}_{teacher_name}"),
                        ]
                    ]
            reply_markup = InlineKeyboardMarkup(shivabeta)
            await query.message.edit_text(f"**ーーーーーーーーーーーーーーーーーー**\n\n**Lectures for chapter {chapter_name} obtained successfully from database!! 🎊 **\n\n**Click on the below button to get all lectures...**\n\n**ーーーーーーーーーーーーーーーーーー**", reply_markup= reply_markup )
        else:
            await query.message.reply_text("𝙵𝙰𝙸𝙻𝙴𝙳 𝚃𝙾 𝙵𝙴𝚃𝙲𝙷 𝙻𝙴𝙲𝚃𝚄𝚁𝙴 𝙻𝙸𝙽𝙺, 𝙿𝙻𝙴𝙰𝚂𝙴 𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽 𝙻𝙰𝚃𝙴𝚁.")
    
    elif query.data.startswith("prev_page_"):
        # Handle previous page callback
        subject, teacher_name, previous_page = query.data.split("_")[2:]
        previous_page = int(previous_page)
        await send_previous_page(query.message, subject, teacher_name, previous_page, query)
    elif query.data.startswith("next_page_"):
        # Handle next page callback
        subject, teacher_name, nxt_page = query.data.split("_")[2:]
        nxt_page = int(nxt_page)
        await send_next_page(query.message, subject, teacher_name, nxt_page, query)


async def send_previous_page(message, subject, teacher_name, previous_page, query):
    try:
        # Fetch the chapters for the previous page
        response = await get_chapters(subject, teacher_name)
        try:
            if response:
                chapters = response.get("chapters", [])
            else:
                await message.reply_text("𝙵𝙰𝙸𝙻𝙴𝙳 𝚃𝙾 𝙵𝙴𝚃𝙲𝙷 𝙲𝙷𝙰𝙿𝚃𝙴𝚁𝚂, 𝙿𝙻𝙴𝙰𝚂𝙴 𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽 𝙻𝙰𝚃𝙴𝚁.")
                return
        except ButtonDataInvalid as bd:
            print('ButtonDataInvalid:', bd)
        except Exception as e:
            print('Exception:', e)        
        
    except Exception as c:
        await message.reply_text(f"Failed to fetch chapters. Please try again later. Exception: {c}")
        return

    # Send the chapters for the previous page
    await send_chapters_pages(message, chapters, subject, teacher_name, previous_page, query)


async def send_next_page(message, subject, teacher_name, nxt_page, query):
    # Calculate the next page number
    next_page = nxt_page

    # Fetch the chapters for the next page
    response = await get_chapters(subject, teacher_name)
    try:
        if response:
            chapters = response.get("chapters", [])
        else:
            print('Error fetching chapters')
            return
    except Exception as c:
        await message.reply_text(f"Failed to fetch chapters. Please try again later. Exception: {c}")
        return

    # Send the chapters for the next page
    await send_chapters_pages(message, chapters, subject, teacher_name, next_page, query)


async def send_chapters_pages(message, chapters, subject, teacher_name, current_page, previous_page=None, next_page=None, query: CallbackQuery = None):
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
        pagination_buttons.append(InlineKeyboardButton(" ☚", callback_data=f"prev_page_{subject}_{teacher_name}_{current_page - 1}"))
    if current_page == 1:
        xytra = total_pages
        pagination_buttons.append(InlineKeyboardButton(" ☚", callback_data=f"prev_page_{subject}_{teacher_name}_{xytra}"))
    pagination_buttons.append(InlineKeyboardButton("❉ 𝐓𝙴𝙰𝙲𝙷𝙴𝚁𝚂 ❉",  callback_data=f"subject_{subject}"))
    if current_page < total_pages:
        pagination_buttons.append(InlineKeyboardButton("☛", callback_data=f"next_page_{subject}_{teacher_name}_{current_page + 1}"))
    if current_page == total_pages:
        radiux = 1
        pagination_buttons.append(InlineKeyboardButton("☛", callback_data=f"next_page_{subject}_{teacher_name}_{radiux}"))
    buttons.append(pagination_buttons)
    
    try:
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.edit_text(f"Page {current_page}/{total_pages} - Please choose a chapter from below buttons:", reply_markup=reply_markup)
    except ButtonDataInvalid:
        await message.reply_text(f"InlineButton text too long.\n\n Please report it to support chat")
    except MessageNotModified:
        await query.answer("Their is no other pages!!")
    except rpc_error as e:
        await message.reply_text(f"An error occured: {e}\n\n Please report it to support chat!!")



# @Bot.on_message(filters.command('lecture') & filters.group)
# async def lectures_command(client, message):
#     BOT_USERNAME = config.BOT_USERNAME
#     markup = InlineKeyboardMarkup([
#     [InlineKeyboardButton("𝐔ᴘᴅᴀᴛᴇs", url=config.UPDATE),
#     InlineKeyboardButton("𝐒ᴜᴘᴘᴏʀᴛ", url=config.SUPPORT)],
#     [InlineKeyboardButton("𝐔sᴇ ᴍᴇ ɪɴ ᴘᴍ", url=f"t.me/{BOT_USERNAME}?start")]    
#     ]) 
#     # Send the message with the inline keyboard
#     await message.reply_text("𝐈 𝐂𝙰𝙽 𝐎𝙽𝙻𝚈 𝐁𝙴 𝐔𝚂𝙴𝙳 𝐈𝙽 𝐓𝙷𝙴 𝐏𝚁𝙸𝚅𝙰𝚃𝙴 𝐌𝙾𝙳𝙴 !!", reply_markup=markup)
