import pyrostep
from pyrogram import filters
from pyrogram.types import Message
from zenova import zenova
from config2 import LOGGER_ID

pyrostep.listen(zenova)
@zenova.on_message(filters.command("feedback"))
async def feedback(client, message: Message):
    await message.reply_text("Please enter your feedback now:")

    # Wait for the user to send the feedback message
    feedback_msg: Message = await pyrostep.wait_for(message.from_user.id)
    try:
        if feedback_msg:
            sent_msg = await client.forward_messages(LOGGER_ID, message.from_user.id, message.id)
            user_info = f"User ID: {message.from_user.id}\nUsername: @{message.from_user.username}"
            feedback_info = (
                f"📣 New Feedback! 📣\n\n{user_info}"
            )
            await client.send_message(LOGGER_ID, feedback_info, reply_to_message_id= sent_msg.id)
            await message.reply_text("Thanks for your feedback! It has been sent to the team.")
        else:
            await message.reply_text("Your feedback message cannot be empty. Please try again.")
    except Exception as e:
        try:
            await client.send_message(LOGGER_ID, e)
        except:
            print(f"An error caught during sending feedback to log channel!! Please chack log channel id properly. Error:{e}")
