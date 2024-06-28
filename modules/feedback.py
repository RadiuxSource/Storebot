import pyrostep
from pyrogram import filters
from zenova import zenova
from config2 import LOGGER_ID

pyrostep.listen(zenova)
@zenova.on_message(filters.command("feedback"))
async def feedback(client, message):
    await message.reply_text("Please enter your feedback now:")

    # Wait for the user to send the feedback message
    feedback_msg = await pyrostep.wait_for(message.chat.id)
    feedback_text = feedback_msg.text
    try:
        if feedback_text:
            user_info = f"User ID: {message.from_user.id}\nUsername: @{message.from_user.username}"
            feedback_info = (
                f"📣 New Feedback! 📣\n\n{user_info}\n\nFeedback: {feedback_text}"
            )
            log_channel = LOGGER_ID
            await client.send_message(log_channel, feedback_info)
            await message.reply_text("Thanks for your feedback! It has been sent to the team.")
        else:
            await message.reply_text("Your feedback message cannot be empty. Please try again.")
    except Exception as e:
        try:
            await client.send_message(log_channel, e)
        except:
            print(f"An error caught during sending feedback to log channel!! Please chack log channel id properly. Error:{e}")
