"""
Add Me In Bot 

Taught and documented by: 
Ryo and Peng Fei from RC4Space 

"""

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Set up INFO_STORE to store user data 
INFO_STORE = {}
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
    user = update.message.from_user
    chatid = update.message.chat.id

    log_text = "User " + str(user.id) + " has started creating poll"
    print(log_text) # To keep track of log

    # context.args the arguments are in a list! Thus need to convert to a string. 
    poll_question_text = ' '.join(context.args)

    # Increase the poll number and initialise this poll data storage
    global POLL_NUMBER
    POLL_NUMBER += 1

    # set up INFO_STORE for this poll number 
    INFO_STORE[POLL_NUMBER] = {}

    # Link the poll number to the poll question text
    INFO_STORE[POLL_NUMBER]["poll_question"] = poll_question_text

    # Set up a dictionary containing poll options to be added 
    INFO_STORE[POLL_NUMBER][poll_question_text] = {}

    # set up INFO_STORE for this user 
    INFO_STORE[user.id] = {}

    # Link the current poll number to this user
    INFO_STORE[user.id]["current_poll_number"] = POLL_NUMBER
    
    reply_text = "Your poll question is: " + poll_question_text 
    reply_text += "\n\nNext, to add your first poll option, send in the format of /add POLL OPTION:"
    reply_text += "\n\nExample: /add Bubble tea"

    context.bot.send_message(text = reply_text,
                            chat_id = chatid,
                            parse_mode=ParseMode.HTML)
    return 


def add_poll_option(update, context):
    user = update.message.from_user
    chatid = update.message.chat.id

    log_text = "User " + str(user.id) + " has added a poll option"
    print(log_text) # To keep track of log

    # Get the poll option text from the arguments
    new_poll_option_text = ' '.join(context.args)

    # Get the current poll number 
    POLL_NUMBER = INFO_STORE[user.id]["current_poll_number"] 
    
    # Get the poll question linked to this poll number
    poll_question_text = INFO_STORE[POLL_NUMBER]["poll_question"] 

    # Store poll option for this poll question (with a unique poll number)
    INFO_STORE[POLL_NUMBER][poll_question_text][new_poll_option_text] = [] # Set up an empty list as a 'value' for the option 'key'
    
    reply_text = "Okay you have added this as a poll option: " + new_poll_option_text 
    reply_text += "\n\nAdd another poll option? Send in the format of /add POLL OPTION:"
    reply_text += "\nExample: /add Coffee"
    reply_text += "\n\nPress /done to complete the poll."

    context.bot.send_message(text = reply_text,
                            chat_id = chatid,
                            parse_mode=ParseMode.HTML)
    return


def done(update, context):
    user = update.message.from_user
    chatid = update.message.chat.id

    log_text = "User " + str(user.id) + " has pressed done to complete poll questions"
    print(log_text) # To keep track of log

    reply_text = "Okay your poll is created! Here is it!"

    context.bot.send_message(text = reply_text,
                            chat_id = chatid,
                            parse_mode=ParseMode.HTML)

    # Get the current poll number 
    POLL_NUMBER = INFO_STORE[user.id]["current_poll_number"] 
    
    # Get the poll question linked to this poll number
    poll_question_text = INFO_STORE[POLL_NUMBER]["poll_question"] 

    # Get every poll option out as a list
    poll_options_list = list(INFO_STORE[POLL_NUMBER][poll_question_text].keys())

    # Gather the question and options into nice format
    poll_text = "<b>" + poll_question_text + "</b>"

    # Initialising an empty button list:
    button_list = []
    
    # For loop to go through every option in the options list in order to add the option text 
    # Also adds the option as a button!
    for option in poll_options_list:
        poll_text += "\n\n<b>" + option + ":</b>"
        data_to_be_sent = str(POLL_NUMBER) + "_" + option
        button_list.append(InlineKeyboardButton(text = option, callback_data = data_to_be_sent))

    # Then make the button list into a buttons menu for Telegram 
    menu = build_menu(button_list, n_cols = 1, header_buttons = None, footer_buttons = None)

    print("Created poll number: {}".format(str(POLL_NUMBER)))

    context.bot.send_message(text = poll_text,
                            chat_id = chatid,
                            parse_mode=ParseMode.HTML,
                            reply_markup = InlineKeyboardMarkup(menu)) # Add a reply markup to include the buttons!
    return 


def update_poll(update, context):
    user = update.callback_query.from_user
    chatid = update.callback_query.message.chat_id
    current_message_id = update.callback_query.message.message_id
    data_received = update.callback_query.data

    # max parameter is set to 1, thus, it will only split into 2 items in the list
    processed_data_list = data_received.split("_", 1) 

    # Get the option pressed 
    option_pressed = processed_data_list[1]

    # Get the associated poll number for this button pressed 
    POLL_NUMBER = int(processed_data_list[0])
    print("Updating poll number: {}".format(str(POLL_NUMBER)))
    
    # Get the poll question linked to this poll number
    poll_question_text = INFO_STORE[POLL_NUMBER]["poll_question"] 

    # Get every poll option out as a list
    poll_options_list = list(INFO_STORE[POLL_NUMBER][poll_question_text].keys())

    # Update the info store with the name of the user who pressed this option
    name = user.first_name
    current_names_list = INFO_STORE[POLL_NUMBER][poll_question_text][option_pressed]
    if name in current_names_list:
        INFO_STORE[POLL_NUMBER][poll_question_text][option_pressed].remove(name) # removes the first matching name (this is a flaw)
    else:
        INFO_STORE[POLL_NUMBER][poll_question_text][option_pressed].append(name)
    
    # Gather the question and options into nice format
    poll_text = "<b>" + poll_question_text + "</b>"

    # Initialising an empty button list:
    button_list = []
    
    # For loop to go through every option in the options list in order to add the option text 
    # Also adds the option as a button!
    for option in poll_options_list:
        poll_text += "\n\n<b>" + option + ":</b>"
    
        option_name_list = INFO_STORE[POLL_NUMBER][poll_question_text][option]

        # insert all the current names below!
        for name in option_name_list:
            poll_text += "\n" + name 

        data_to_be_sent = str(POLL_NUMBER) + "_" + option
        button_list.append(InlineKeyboardButton(text = option, callback_data = data_to_be_sent))

    # Then make the button list into a buttons menu for Telegram 
    menu = build_menu(button_list, n_cols = 1, header_buttons = None, footer_buttons = None)

    context.bot.edit_message_text(text = poll_text,
                                chat_id = chatid,
                                parse_mode=ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menu), # Add a reply markup to include the buttons!
                                message_id = current_message_id) # message id to indicate which message for the bot to edit!
    return 


# A function to build menu of buttons for every occasion 
def build_menu(buttons, n_cols, header_buttons, footer_buttons):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu



def main():   
    # Telegram bot token from BotFather, very important do not lose it or reveal it:
    TELEGRAM_TOKEN = "1326912451:AAE2RHt07w-NoekNI8szvbe2U9-mRW1ZQ_M"
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

    # Callback handler to handle data sent when anyone presses a button for an option
    dispatcher.add_handler(CallbackQueryHandler(callback = update_poll))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
