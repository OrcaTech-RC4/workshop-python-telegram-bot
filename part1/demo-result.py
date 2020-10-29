from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import random

def hail(update, context):
    chat_id = update.message.chat.id
    username = update.message.from_user.username

    text = "All hail the magic conch shell! 🐚\nRate me please, " + username + "!"

    rating_buttons = [[KeyboardButton(text=i) for i in range(1,6)]]

    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=ReplyKeyboardMarkup(keyboard=rating_buttons, one_time_keyboard=True)
    )

    return 1

def get_rating_ask_feedback(update, context):
    chat_id = update.message.chat.id
    user_input = update.message.text

    # If user input is not valid, prompt for ratings
    if not user_input.isdigit() or not int(user_input) in range(1,6):
        rating_buttons = [[KeyboardButton(text=i) for i in range(1,6)]]

        context.bot.send_message(
            chat_id=chat_id,
            reply_markup=ReplyKeyboardMarkup(keyboard=rating_buttons, one_time_keyboard=True)
        )

        return 1
    
    text = "Thanks for rating me " + user_input + "!\nPlease enter a short feedback for me!"

    context.bot.send_message(
        text=text,
        chat_id=chat_id
    )
    return 2

def get_feedback_end(update, context):
    chat_id = update.message.chat.id
    user_input = update.message.text

    text = "This is your submitted feedback! Thanks!\n" + user_input

    context.bot.send_message(
        text=text,
        chat_id=chat_id
    )

    return ConversationHandler.END

def ask(update, context):
    chat_id = update.message.chat.id
    user_text = update.message.text

    if user_text[-1] == "?":

        answer = "Yes" if (random.random() > 0.5) else "No"

        if not context.chat_data.get("history"):
            context.chat_data["history"] = [user_text.replace("/ask ", "", 1) + answer]
        else:
            context.chat_data["history"].append(user_text.replace("/ask ", "", 1) + answer)

        print(context.chat_data)

        context.bot.send_message(
            text=answer,
            chat_id=chat_id
        )
        return

    context.bot.send_message(
        text="Send me a question ASAP! Ending with ?",
        chat_id=chat_id
    )

def history(update, context):
    chat_id = update.message.chat.id
    
    context.bot.send_message(
        text="\n".join(context.chat_data["history"]),
        chat_id=chat_id
    )

def start(update, context):
    print("UPDATE:", update)
    print("CONTEXT:", context)

    chat_id = update.message.chat.id
    text = "Hello " + update.message.from_user.first_name + ",I'm orcatech bot!"

    context.bot.send_message(
        text=text,
        chat_id=chat_id
    )

def main():
    # Get telegram bot token from botfather, and do not lose or reveal it
    # TODO: Change below to your bot token
    BOT_TOKEN = "1326912451:AAE2RHt07w-NoekNI8szvbe2U9-mRW1ZQ_M"

    # bot updater, refer to https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.updater.html
    updater = Updater(BOT_TOKEN, use_context=True)
    
    # bot dispatcher to register command handlers
    dp = updater.dispatcher

    # put your handlers here
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ask", ask))
    dp.add_handler(CommandHandler("history", history))

    dp.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("hail", hail)],
            states={
                1: [MessageHandler(Filters.text, get_rating_ask_feedback)],
                2: [MessageHandler(Filters.text, get_feedback_end)]
            },
            fallbacks=[],
            per_user=False
        )
    )

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()