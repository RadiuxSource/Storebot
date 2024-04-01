import re
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import Bot

@Bot.on_message(filters.command('lecture'))
async def lectures_command(client, message):
    # Create the inline keyboard with subjects
    keyboard = [
        [
            InlineKeyboardButton("Physics", callback_data="subject_physics"),
            InlineKeyboardButton("Maths", callback_data="subject_maths"),
        ],
        [
            InlineKeyboardButton("Organic Chemistry", callback_data="subject_organic"),
            InlineKeyboardButton("Inorganic Chemistry", callback_data="subject_inorganic"),
        ],
        [
            InlineKeyboardButton("Physical Chemistry", callback_data="subject_physical"),
        ]
    ]
    # Create the InlineKeyboardMarkup object
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send the message with the inline keyboard
    await message.reply_text("Choose a subject from below please:", reply_markup=reply_markup)

@Bot.on_callback_query(filters.regex(r'^subject_.*'))
async def subject_callback(_, query):
    print('ok')
    subject = query.data.split("_")[1]
    print('subject:', subject)
    # Fetch data from the API
    response = requests.get(f"https://zenova-lec-api.vercel.app/teachers?subject={subject}")
    if response.status_code == 200:
        teachers_data = response.json()
        # Create inline buttons for each teacher
        buttons = [InlineKeyboardButton(teacher, callback_data=f"teacher_{subject}_{teacher}") for teacher in teachers_data[0]["teachers"]]
        # Add a button for each subject
        buttons.append(InlineKeyboardButton("Choose a subject", callback_data="subject_choice"))
        # Create InlineKeyboardMarkup object with buttons
        reply_markup = InlineKeyboardMarkup([buttons])
        # Edit the callback message to choose a teacher
        await query.message.edit_text(f"Choose a teacher for {subject}:", reply_markup=reply_markup)
    else:
        await query.message.edit_text("Failed to fetch data from the API. Please try again later.")

@Bot.on_callback_query(filters.regex(r'^teacher_.*'))
async def teacher_callback(_, query):
    data_parts = re.split(r'_', query.data)
    subject = data_parts[1]
    teacher_name = data_parts[2]
    # Fetch data from the API for chapters
    response = requests.get(f"https://zenova-lec-api.vercel.app/chapters?subject={subject}&teacher={teacher_name}")
    if response.status_code == 200:
        chapters_data = response.json()
        # Create inline buttons for each chapter
        buttons = [InlineKeyboardButton(chapter, callback_data=f"chapter_{subject}_{teacher_name}_{chapter}") for chapter in chapters_data["chapters"]]
        # Create InlineKeyboardMarkup object with buttons
        reply_markup = InlineKeyboardMarkup([buttons])
        # Edit the callback message to choose a chapter
        await query.message.edit_text("Please choose a chapter from below buttons:", reply_markup=reply_markup)
    else:
        await query.message.edit_text("Failed to fetch data from the API. Please try again later.")

@Bot.on_callback_query(filters.regex(r'^chapter_.*'))
async def chapter_callback(_, query):
    data_parts = re.split(r'_', query.data)
    subject = data_parts[1]
    teacher_name = data_parts[2]
    chapter_name = data_parts[3]
    # Fetch data from the API for the lecture link
    response = requests.get(f"https://zenova-lec-api.vercel.app/lecture?subject={subject}&teacher={teacher_name}&ch={chapter_name}")
    if response.status_code == 200 and response.json()["success"]:
        lecture_link = response.json()["link"]
        # Send the lecture link to the user
        await query.message.reply_text(f"Here's the lecture link for {chapter_name} by {teacher_name}: {lecture_link}")
    else:
        await query.message.reply_text("Failed to fetch lecture link. Please try again later.")
