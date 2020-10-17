from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def echo(update, context):
    chat_id = update.message.chat.id
    text = update.message.text

    context.bot.send_message(
        text=text, 
        chat_id=chat_id
        )

def start(update, context):
    print("UPDATE:", update)
    print("CONTEXT:", context)

def main():
    # Get telegram bot token from botfather, and do not lose or reveal it
    # TODO: Change below to your bot token
    BOT_TOKEN = "1163718245:AxxxAHmjtOxxVc2TZe-Bn-B9xxxkl1GlcWAQ0"

    # bot updater, refer to https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.updater.html
    updater = Updater(BOT_TOKEN, use_context=True)
    
    # bot dispatcher to register command handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()