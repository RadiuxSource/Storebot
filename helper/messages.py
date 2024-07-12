from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config2 as config


START_TXT= """👋 **Wᴇʟᴄᴏᴍᴇ ᴛᴏ Zᴇɴᴏᴠᴀ Lᴇᴄᴛᴜʀᴇs Bᴏᴛ!**

Get ready for an enriching learning experience with free lectures from various teachers!

📚 **𝐁ʀᴏᴡsᴇ 𝐒ᴜʙᴊᴇᴄᴛs**: **Explore lectures on Physics, Maths, Organic Chemistry, and more.**

🎓 **𝐄xᴘᴇʀᴛ 𝐓ᴇᴀᴄʜᴇʀs**: **Learn from experienced educators who cover essential topics.**

💡 **𝐍ᴇᴇᴅ 𝐇ᴇʟᴘ?** **Visit our support group for assistance.**

**Use /help to know more.**

Enjoy your learning journey with us! 🚀📖
"""


NOTICE_TXT = """
🚨 Attention! Your Feedback Needed! 🚨

Hey there! We're constantly looking to improve our bot, and we need YOUR input! Besides lectures, what new features would you like to see? Use the /feedback command to share your ideas and suggestions.
Also you can request any type of lectures, courses, material to be available in the shop at most affordable way possible.

💡 Your ideas can make a difference! 💡
"""



START_BTN = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🕵️‍♂️ 𝐇ᴇʟᴘ", url=f"https://t.me/Jee_lecture_bot/zenova_ai"),
        InlineKeyboardButton("📜 𝐂ᴏᴍᴍᴀɴᴅs", callback_data="commands")
    ],
    [InlineKeyboardButton("𝐔ᴘᴅᴀᴛᴇs", url=config.UPDATE),
    InlineKeyboardButton("𝐒ᴜᴘᴘᴏʀᴛ", url=config.SUPPORT)],
    [InlineKeyboardButton("𝐀ᴅᴅ 𝐌ᴇ 𝐓ᴏ 𝐘ᴏᴜʀ 𝐆ʀᴏᴜᴘ!", url=config.Bot_join_url)]
])


CMD_LIST = """
**List of commands in this bot:**

**/start** : Start the bot 💝

**/help** : Get help and information about the bot 💘

**/lecture** : Get lectures of different subjects and teachers ❣️

**/shop** : Get paid courses, Mentorship, Membership at affordable prices ❤‍🩹

**/quiz on/off** : Get hourly quizes in your gropus 💕

**/feedback** : Share your feedbacks or request paid materials 💌

**/ping** : Check weather bot is alive or not 💖

"""


HELP_MSG = '''Hello! 🤗 Need some help with Zenova Lectures Bot? Here are some tips to get you started:

🔹 Firstly, Start our Companion bot by clicking on the below button.

🔹 **Browse Lectures**: Find lectures on various subjects, including Physics, Maths, Organic Chemistry, and more. Simply type /lecture to view the list.

🔹 **Feedback**: We'd love to hear your thoughts! Share your feedback with us at support group.

🔹 **Help and Support**: If you need assistance, visit our support group or type /help.

👉 For a list of all available commands, click the "📜 𝐂ᴏᴍᴍᴀɴᴅs" button below.

**Happy learning with Zenova Lectures Bot! 📚🚀**'''



companion_bot_url = config.LEC_BOT


HELP_MARKUP = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🏠 𝐇ᴏᴍᴇ", callback_data="home"),
        InlineKeyboardButton("📜 𝐂ᴏᴍᴍᴀɴᴅs", callback_data="commands")
    ],
    [
        InlineKeyboardButton("𝐔ᴘᴅᴀᴛᴇs", url=config.UPDATE),
        InlineKeyboardButton("𝐒ᴜᴘᴘᴏʀᴛ", url=config.SUPPORT)
    ],
    [
        InlineKeyboardButton("𝐂ᴏᴍᴘᴀɴɪᴏɴ 𝐁ᴏᴛ", url=companion_bot_url)
    ]
])



CMD_MARKUP = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🏠 𝐇ᴏᴍᴇ", callback_data="home"),
        InlineKeyboardButton("🕵️‍♂️ 𝐇ᴇʟᴘ", callback_data="help_back")
    ]
])



SUBJECTS_BTN = [
    [
        InlineKeyboardButton("𝐏𝙷𝚈𝚂𝙸𝙲𝚂", callback_data="subject_physics"),
        InlineKeyboardButton("𝐌𝙰𝚃𝙷𝚂", callback_data="subject_maths"),
    ],
    [
        InlineKeyboardButton("𝐎𝚁𝙶𝙰𝙽𝙸𝙲 𝐂𝙷𝙴𝙼𝙸𝚂𝚃𝚁𝚈", callback_data="subject_organic"),
        InlineKeyboardButton("𝐈𝙽𝙾𝚁𝙶𝙰𝙽𝙸𝙲 𝐂𝙷𝙴𝙼𝙸𝚂𝚃𝚁𝚈", callback_data="subject_inorganic"),
    ],
    [
        InlineKeyboardButton("𝐏𝙷𝚈𝚂𝙸𝙲𝙰𝙻 𝐂𝙷𝙴𝙼𝙸𝚂𝚃𝚁𝚈", callback_data="subject_physical"),
    ]
]
