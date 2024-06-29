from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config2 as config

START_TXT = """👋 **Welcome to Zenova Lectures Bot!**

Get ready for an enriching learning experience with free lectures from various teachers!

📚 **Browse Subjects**: **Explore lectures on Physics, Maths, Organic Chemistry, and more.**

🎓 **Expert Teachers**: **Learn from experienced educators who cover essential topics.**

💡 **Need Help?** **Visit our support group for assistance.**

```Use /help to know more.```

Enjoy your learning journey with us! 🚀📖
"""

NOTICE_TXT = """
```🚨 Attention! Your Feedback Needed! 🚨

Hey there! We're constantly looking to improve our bot, and we need YOUR input! Besides lectures, what new features would you like to see? Use the /feedback command to share your ideas and suggestions.

💡 Your ideas can make a difference! 💡```
"""

START_BTN = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🕵️‍♂️ Help", callback_data="help_back"),
        InlineKeyboardButton("📜 Commands", callback_data="commands")
    ],
    [InlineKeyboardButton("Updates", url=config.UPDATE),
     InlineKeyboardButton("Support", url=config.SUPPORT)],
    [InlineKeyboardButton("Add Me To Your Group!", url=config.Bot_join_url)]
])

CMD_LIST = """
```List of commands in this bot:

/start - Start the bot

/help - Get help and information about the bot

/lecture - Get lectures of different subjects and teachers

/feedback - To share your feedbacks.

/ping - Check whether bot is alive or not```
"""

HELP_MSG = '''Hello! 🤗 Need some help with Zenova Lectures Bot? Here are some tips to get you started:

🔹 Firstly, Start our Companion bot by clicking on the below button.

🔹 **Browse Lectures**: Find lectures on various subjects, including Physics, Maths, Organic Chemistry, and more. Simply type /lecture to view the list.

🔹 **Feedback**: We'd love to hear your thoughts! Share your feedback with us at support group.

🔹 **Help and Support**: If you need assistance, visit our support group or type /help.

👉 For a list of all available commands, click the "📜 Commands" button below.

**Happy learning with Zenova Lectures Bot! 📚🚀**
'''

companion_bot_url = config.LEC_BOT

HELP_MARKUP = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🏠 Home", callback_data="home"),
        InlineKeyboardButton("📜 Commands", callback_data="commands")
    ],
    [
        InlineKeyboardButton("Updates", url=config.UPDATE),
        InlineKeyboardButton("Support", url=config.SUPPORT)
    ],
    [
        InlineKeyboardButton("Companion Bot", url=companion_bot_url)
    ]
])

CMD_MARKUP = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🏠 Home", callback_data="home"),
        InlineKeyboardButton("🕵️‍♂️ Help", callback_data="help_back")
    ]
])

SUBJECTS_BTN = [
    [
        InlineKeyboardButton("PHYSICS", callback_data="subject_physics"),
        InlineKeyboardButton("MATHS", callback_data="subject_maths"),
    ],
    [
        InlineKeyboardButton("ORGANIC CHEMISTRY", callback_data="subject_organic"),
        InlineKeyboardButton("INORGANIC CHEMISTRY", callback_data="subject_inorganic"),
    ],
    [
        InlineKeyboardButton("PHYSICAL CHEMISTRY", callback_data="subject_physical"),
    ]
]

