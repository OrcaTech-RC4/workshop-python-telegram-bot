"""
Add Me In Bot 

Taught and documented by: 
Ryo and Peng Fei from RC4Space 

"""

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, InlineQueryHandler

# Set up POLL_NUMBER to keep track of poll id
POLL_NUMBER = 0

def start(update, context):
    user = update.message.from_user
    chatid = update.message.chat.id

    log_text = "User " + str(user.id) + " has started using bot."
    print(log_text) # To keep track of log

    reply_text = "Hello! Welcome to Add Me In Bot! Send /create POLL QUESTION in this format to create a new poll!"
    reply_text += "\n\nExample: /create What drink do you want?"

    context.bot.send_message(text = reply_text,
                            chat_id = chatid,
                            parse_mode=ParseMode.HTML)
    return 


def create(update, context):
    return


def add_poll_option(update, context):
    return

def done(update, context):
    return 

def poll_inline_query_handler(update, context):

def update_poll(update, context):
    return 


# A function to build menu of buttons for every occasion 
def build_menu(buttons, n_cols, header_buttons, footer_buttons):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def error(update, context):
    print("Error occured", context.error)

def main():   
    # Telegram bot token from BotFather, very important do not lose it or reveal it:
    TELEGRAM_TOKEN = "###"
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Dispatching the command for /start
    dispatcher.add_handler(CommandHandler('start', start))

    # Dispatching the command for /create (with arguments as poll question)
    dispatcher.add_handler(CommandHandler('create', create))

    # To handle every single message regarding poll option
    dispatcher.add_handler(CommandHandler('add', add_poll_option))

    # Dispatching the command for /done 
    dispatcher.add_handler(CommandHandler('done', done))

    dispatcher.add_error_handler(error)


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
