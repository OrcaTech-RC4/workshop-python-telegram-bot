from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
import random

def easter_egg(update, context):
    chat_id = update.message.chat.id
    
    text = "The magic conch shell is proud of its followers! It wants to know your name!🐚"

    context.bot.send_message(
        text=text, 
        chat_id=chat_id
        )
    return 2

def show_names(update, context):
    chat_id = update.message.chat.id
    user_input = update.message.text # the user should input his name

    followers = context.chat_data.get("followers")
    
    if not followers:
        followers = [user_input]
        text = "You are my first follower!🐚"
    else:
        text = "Now you are officially my follower🐚, along with:\n" + "\n".join(followers)
        followers.append(user_input)
        


    context.bot.send_message(
        text=text, 
        chat_id=chat_id
    )

    context.chat_data["followers"] = followers

    return ConversationHandler.END

def answer(update, context):
    chat_id = update.message.chat.id
    text = update.message.text

    # Checks if user message text is a question.
    if text[-1] == "?":
        answer = "yes" if (random.random() > 0.5) else "no"

        context.bot.send_message(
            text=answer, 
            chat_id=chat_id
        )
        return ConversationHandler.END
    
    context.bot.send_message(
            text="Send me a question instead!", 
            chat_id=chat_id
        )


def ask(update, context):
    chat_id = update.message.chat.id
    text = "Send me a question--All hail the magic conch shell!🐚"

    context.bot.send_message(
        text=text, 
        chat_id=chat_id
        )

    return 0

def fallback(update, context):
    chat_id = update.message.chat.id
    text = "Use the command /ask to ask me--All hail the magic conch shell!🐚"

    context.bot.send_message(
        text=text, 
        chat_id=chat_id
        )

def start(update, context):
    print("UPDATE:", update)
    print("CONTEXT:", context)

def main():
    # Get telegram bot token from botfather, and do not lose or reveal it
    BOT_TOKEN = "1163718245:AAHmjtOregT9hVc2TZe-Bn-B9kl1GlcWAQ0"

    # bot updater, refer to https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.updater.html
    updater = Updater(BOT_TOKEN, use_context=True)
    
    # bot dispatcher to register command handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(
        ConversationHandler(
            [CommandHandler("ask", ask)],
            {
                0: [
                        CommandHandler("hail", easter_egg), 
                        MessageHandler(Filters.text, answer)
                    ],
                2: [MessageHandler(Filters.text, show_names)]
            },
            []
        )
    )

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()