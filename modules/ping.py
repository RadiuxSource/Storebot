import random
from pyrogram import filters
from zenova import zenova

# yaha ping wali img ki url daal do
ping_img_url = "https://i.ytimg.com/vi/PykvjRcbA_w/sddefault.jpg"

@zenova.on_message(filters.command("ping"))
async def ping(client, message):
    ping_time = round(random.uniform(60, 200), 2)
    ping_msg = f"📍 Pong! 📍\n\n🏓 Ping time: {ping_time} ms"
    await message.reply_photo(ping_img_url, caption=ping_msg)
