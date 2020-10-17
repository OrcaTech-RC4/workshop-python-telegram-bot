from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
import random

followers = []

def hail(update, context):

    print(f"User {update.message.from_user.username} entered the command /hail.")

    username = update.message.from_user.username
    
    text = "All hail the magic conch shell!🐚\n"

    if not followers:
        text += f"You are my first follower, {username}!"
        followers.append(username)
    else:
        text += f"Now you are officially my follower, {username}, along with:\n" + "\n".join(followers)
        followers.append(username)

    context.bot.send_message(
        text=text, 
        chat_id=update.message.chat_id
        )

    # Some feedback feature with keyboard button
    rating_buttons = [[KeyboardButton(text=i) for i in range(1,6)]]

    context.bot.send_message(
        text="Rate me please!", 
        chat_id=update.message.chat_id,
        reply_markup=ReplyKeyboardMarkup(keyboard=rating_buttons, one_time_keyboard=True)
        )
    return 1

def get_rating_ask_feedback(update, context):

    user_input = update.message.text # the user's rating from /hail keyboardbutton

    if not user_input.isdigit() or not int(user_input) in range(1,6):

        # Some feedback feature with keyboard button
        rating_buttons = [[KeyboardButton(text=i) for i in range(1,6)]]
        context.bot.send_message(
            text="Select a proper rating from the options below!", 
            chat_id=update.message.chat_id,
            reply_markup=ReplyKeyboardMarkup(keyboard=rating_buttons, one_time_keyboard=True)
        )
        return 1

    # if value rated correctly, save rating and ask for feedback
    context.user_data["rating"] = int(user_input)

    text = "Enter your feedback now:"
    context.bot.send_message(
        text=text, 
        chat_id=update.message.chat_id
    )
    return 2

def get_feedback_end(update, context):

    user_input = update.message.text # the user's feedback

    context.user_data["feedback"] = user_input

    text = "Thank you for the feedback! All hail the magic conch shell!🐚"
    context.bot.send_message(
        text=text, 
        chat_id=update.message.chat_id
    )
    return ConversationHandler.END

def ask(update, context):

    print(f"User {update.message.from_user.username} entered the command /ask.")

    user_message = update.message.text

    # Checks if user message text is a question.
    if user_message[-1] == "?":
        
        # A simple code with 50:50 chance
        answer = "Yes" if (random.random() > 0.5) else "No"

        context.bot.send_message(
            text=answer, 
            chat_id=update.message.chat_id
        )

        # Append to history per chat if it exists
        if not context.chat_data.get("history"):
            context.chat_data["history"] = []

        context.chat_data["history"].append(
            user_message.replace("/ask ", "", 1) + " " + answer
            )

        print(context.chat_data)

        return
    
    context.bot.send_message(
            text="Send me a question instead!\ne.g. /ask Is Covid gonna end this year?", 
            chat_id=update.message.chat_id
        )

def history(update, context):

    text = "Your questions to the magic conch shell!🐚\n"
    text += "\n".join(context.chat_data["history"]) if context.chat_data.get("history") else "No questions yet..."

    context.bot.send_message(
        text=text, 
        chat_id=update.message.chat_id
        )

def start(update, context):
    
    print("UPDATE:", update)
    print("CONTEXT:", context)

    print(f"User {update.message.from_user.username} started the bot.")

    # Sends a simple message to user, parsed in HTML
    # Reference https://core.telegram.org/bots/api#html-style 
    context.bot.send_message(
        text="Hello! I am the <b>magic conch shell bot</b>. Here are some commands you can try!\n" \
            "<code>/ask Yes/No Question?</code>\n" \
            "<code>/history</code>"\
            "<code>/hail</code>",
        chat_id=update.message.chat_id,
        parse_mode=ParseMode.HTML
    )

def error(update, context):
    print("Error occured", context.error)

def main():
    # Get telegram bot token from botfather, and do not lose or reveal it
    # TODO: Change below to your bot token
    BOT_TOKEN = "1163718245:AxxxAHmjtOxxVc2TZe-Bn-B9xxxkl1GlcWAQ0"

    # bot updater, refer to https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.updater.html
    updater = Updater(BOT_TOKEN, use_context=True)
    
    # bot dispatcher to register command handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ask", ask))
    dp.add_handler(CommandHandler("history", history))
    dp.add_handler(
        ConversationHandler(
            [CommandHandler("hail", hail)],
            {
                1: [MessageHandler(Filters.text, get_rating_ask_feedback)],
                2: [MessageHandler(Filters.text, get_feedback_end)]
            },
            [],
            per_user=False
        )
    )
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()