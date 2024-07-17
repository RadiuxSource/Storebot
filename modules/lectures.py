from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ButtonDataInvalid, MessageNotModified, rpc_error

import requests

from zenova import zenova as Bot
from db import add_user, present_user
import config2 as config
from config2 import LOGGER_ID

strt_txt= '''👋 **Wᴇʟᴄᴏᴍᴇ ᴛᴏ Zᴇɴᴏᴠᴀ Lᴇᴄᴛᴜʀᴇs Bᴏᴛ!**

Get ready for an enriching learning experience with free lectures from various teachers!

📚 **Browse Subjects**: Explore lectures on Physics, Maths, Organic Chemistry, and more.

🎓 **Expert Teachers**: Learn from experienced educators who cover essential topics.

💡 **Need Help?** Visit our support group for assistance.

Use /help to know more.

Enjoy your learning journey with us! 🚀📖
'''
Notice_txt = '''
🚨 Attention! Your Feedback Needed! 🚨

Hey there! We're constantly looking to improve our bot, and we need YOUR input! Besides lectures, what new features would you like to see? Use the /feedback command to share your ideas and suggestions.

💡 Your ideas can make a difference! 💡'''

strt_btn = InlineKeyboardMarkup([
    [InlineKeyboardButton("Uᴘᴅᴀᴛᴇs", url=config.UPDATE),
    InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT)],
    [InlineKeyboardButton("Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ!", url=config.Bot_join_url)]
])

commands_list = """
List of commands in this bot:

/start - Start the bot

/help - Get help and information about the bot

/lecture - Get lectures of different subjects and teachers

/feedback - To share your feedbacks.

/ping - Check weather bot is alive or not

"""

help_msg = '''Hello! 🤗 Need some help with Zenova Lectures Bot? Here are some tips to get you started:

🔹 Firstly, Start our Companion bot by clicking on the below button.

🔹 Browse Lectures: Find lectures on various subjects, including Physics, Maths, Organic Chemistry, and more. Simply type /lecture to view the list.

🔹 Feedback: We'd love to hear your thoughts! Share your feedback with us at support group.

🔹 Help and Support: If you need assistance, visit our support group or type /help.

👉 For a list of all available commands, click the "📜 𝐂ᴏᴍᴍᴀɴᴅs" button below.

Happy learning with Zenova Lectures Bot! 📚🚀'''


companion_bot_url = config.LEC_BOT

help_markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🏠 𝐇ᴏᴍᴇ", callback_data="home"),
        InlineKeyboardButton("📜 𝐂ᴏᴍᴍᴀɴᴅs", callback_data="commands")
    ],
    [
        InlineKeyboardButton("Uᴘᴅᴀᴛᴇs", url=config.UPDATE),
        InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT)
    ],
    [
        InlineKeyboardButton("𝐂ᴏᴍᴘᴀɴɪᴏɴ 𝐁ᴏᴛ", url=companion_bot_url)
    ]
])

cmd_markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🏠 𝐇ᴏᴍᴇ", callback_data="home"),
        InlineKeyboardButton("⬅️ 𝐁ᴀᴄᴋ", callback_data="help_back")
    ]
])


gpay = [
    [
        InlineKeyboardButton("߷︎ 𝐏𝙷𝚈𝚂𝙸𝙲𝚂 ߷︎", callback_data="subject_physics"),
        InlineKeyboardButton("߷︎ 𝐌𝙰𝚃𝙷𝚂 ߷︎", callback_data="subject_maths"),
    ],
    [
        InlineKeyboardButton("𝐎𝚁𝙶𝙰𝙽𝙸𝙲 𝐂𝙷𝙴𝙼𝙸𝚂𝚃𝚁𝚈", callback_data="subject_organic"),
        InlineKeyboardButton("𝐈𝙽𝙾𝚁𝙶𝙰𝙽𝙸𝙲 𝐂𝙷𝙴𝙼𝙸𝚂𝚃𝚁𝚈", callback_data="subject_inorganic"),
    ],
    [
        InlineKeyboardButton("߷︎ 𝐏𝙷𝚈𝚂𝙸𝙲𝙰𝙻 𝐂𝙷𝙴𝙼𝙸𝚂𝚃𝚁𝚈߷︎ ", callback_data="subject_physical"),
    ]
]

@Bot.on_message((filters.command(["start"]))) 
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
    await message.reply(Notice_txt)
    await message.reply_photo(config.Start_img, caption= strt_txt, reply_markup=strt_btn)


@Bot.on_message(filters.command("help"))
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
            await client.send_message(LOGGER_ID, INFO)
        except:
            pass
    await message.reply_text(help_msg, reply_markup=help_markup)
   

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
    # Create the InlineKeyboardMarkup object
    reply_markup = InlineKeyboardMarkup(gpay)
    # Send the message with the inline keyboard
    await message.reply_text("𝐂𝙷𝙾𝚂𝙴 𝙰 𝐒𝚄𝙱𝙹𝙴𝙲𝚃 𝐅𝚁𝙾𝙼 𝐁𝙴𝙻𝙾𝚆 𝐏𝙻𝙴𝙰𝚂𝙴 :", reply_markup=reply_markup)

@Bot.on_callback_query()
async def handle_callback(_, query):
    if query.data.startswith("subject_"):
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
            await query.message.edit_text("Failed to fetch data from the API. Please try again later.")
    elif query.data == "subject":
        reply_markup = InlineKeyboardMarkup(gpay)
        await query.message.edit_text("𝐂𝙷𝙾𝚂𝙴 𝙰 𝐒𝚄𝙱𝙹𝙴𝙲𝚃 𝐏𝙻𝙴𝙰𝚂𝙴 :", reply_markup = reply_markup)
    elif query.data.startswith("teacher_"):
        data_parts = query.data.split("_")
        subject = data_parts[1]
        teacher_name = data_parts[2]
        print('teacher name:', teacher_name)
        response = requests.get(f"https://zenova-api-green.vercel.app/chapters?subject={subject}&teacher={teacher_name}")
        try:
            if response.status_code == 200:
                chapters_data = response.json()
                chapters = chapters_data.get("chapters", [])
                current_page = 1
                next_page = 2
                await send_chapters_pages(query.message, chapters, subject, teacher_name, current_page, next_page)
            else:
                await query.message.edit_text("Failed to fetch data from the API. Please try again later.")
        except ButtonDataInvalid as bd:
            print('ButtonDataInvalid:', bd)
        except Exception as e:
            print('Exception:', e)
    elif query.data.startswith("chapter_"):
        data_parts = query.data.split("_")
        subject = data_parts[1]
        teacher_name = data_parts[2]
        chapter_name = data_parts[3]
        response = requests.get(f"https://zenova-api-green.vercel.app/lecture?subject={subject}&teacher={teacher_name}&ch={chapter_name}")
        if response.status_code == 200:
            lecture_link = response.json()["link"]
            shivabeta = [
                        [
                            InlineKeyboardButton("𝐋𝐄𝐂𝐓𝐔𝐑𝐄𝐒", url= lecture_link),
                            InlineKeyboardButton("𝐁𝐀𝐂𝐊", f"teacher_{subject}_{teacher_name}"),
                        ]
                    ]
            reply_markup = InlineKeyboardMarkup(shivabeta)
            await query.message.edit_text(f"Lectures for chapter {chapter_name} obtained successfully from database!!\n\nClick on the below button to get all lectures.", reply_markup= reply_markup )
        else:
            await query.message.reply_text("Failed to fetch lecture link. Please try again later.")
    
    elif query.data.startswith("prev_page_"):
        # Handle previous page callback
        subject, teacher_name, previous_page = query.data.split("_")[2:]
        previous_page = int(previous_page)
        print('previous page:', previous_page)
        await send_previous_page(query.message, subject, teacher_name, previous_page)
    elif query.data.startswith("next_page_"):
        # Handle next page callback
        subject, teacher_name, nxt_page = query.data.split("_")[2:]
        nxt_page = int(nxt_page)
        print('next page:', nxt_page)
        await send_next_page(query.message, subject, teacher_name, nxt_page)
    elif query.data == "home":
        await query.message.edit_caption(strt_txt, reply_markup=strt_btn)
    elif query.data == "commands":
        await query.message.edit_text(commands_list, parse_mode=enums.ParseMode.MARKDOWN, reply_markup=cmd_markup)
    elif query.data == "help_back":    
         await query.message.edit_text(help_msg, reply_markup=help_markup)

async def send_previous_page(message, subject, teacher_name, previous_page):
    print('prev pg')
    try:
        # Fetch the chapters for the previous page
        response = requests.get(f"https://zenova-api-green.vercel.app/chapters?subject={subject}&teacher={teacher_name}")
        try:
            if response.status_code == 200:
                chapters = response.json()["chapters"]
            else:
                await message.reply_text("Failed to fetch chapters. Please try again later.")
                return
        except ButtonDataInvalid as bd:
            print('ButtonDataInvalid:', bd)
        except Exception as e:
            print('Exception:', e)        
        
    except Exception as c:
        await message.reply_text(f"Failed to fetch chapters. Please try again later. Exception: {c}")
        return


    # Send the chapters for the previous page
    await send_chapters_pages(message, chapters, subject, teacher_name, previous_page)
async def send_next_page(message, subject, teacher_name, nxt_page):
    # Calculate the next page number
    next_page = nxt_page

    # Fetch the chapters for the next page
    try:
        response = requests.get(f"https://zenova-api-green.vercel.app/chapters?subject={subject}&teacher={teacher_name}")    
        if response.status_code == 200:
            chapters = response.json()["chapters"]
            print('got it')
        else:
            print('Error fetching chapters')
            return
    except Exception as c:
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
