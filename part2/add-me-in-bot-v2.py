"""
Add Me In Bot 

Taught and documented by: 
Ryo and Peng Fei from RC4Space 

"""

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, InlineQueryHandler

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


    if not poll_question_text.isspace():

        # Increase the poll number and initialise this poll data storage
        global POLL_NUMBER
        POLL_NUMBER += 1

        context.user_data["poll"] = {
            "id": POLL_NUMBER,
            "question":poll_question_text,
            "choices":{}
        }

        print(context.user_data)
        
        reply_text = "Your poll question is: " + poll_question_text 
        reply_text += "\n\nNext, to add your first poll option, send in the format of /add POLL OPTION:"
        reply_text += "\n\nExample: /add Bubble tea"

    else:
        reply_text = "Please enter a non-empty Poll Question!, /create POLL QUESTION"

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
    print(new_poll_option_text)

    context.user_data["poll"]["choices"].update({
        new_poll_option_text: []
        }) # An empty list, to be filled with names for this option

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
    
    # Poll id or poll number
    poll_number = context.user_data["poll"]["id"]

    # Get the poll question linked to this poll number
    poll_question_text = context.user_data["poll"]["question"]

    # Get every poll option out as a list
    poll_options_list = list(context.user_data["poll"]["choices"].keys())

    # Gather the question and options into nice format
    poll_text = "<b>" + poll_question_text + "</b>"

    # Initialising an empty button list:
    button_list = []
    
    # For loop to go through every option in the options list in order to add the option text 
    # Also adds the option as a button!
    for option in poll_options_list:
        poll_text += "\n\n<b>" + option + ":</b>"
        data_to_be_sent = str(poll_number) + "_" + option
        button_list.append(InlineKeyboardButton(text = option, callback_data = data_to_be_sent))

    # Then make the button list into a buttons menu for Telegram 
    menu = build_menu(button_list, n_cols = 1, header_buttons = None, footer_buttons = None)

    # Store the created menu inside a dictionary
    context.user_data["poll"].update({
        "menu": menu
    })

    # Move the data to bot_data
    if not context.bot_data.get("polls"):
        context.bot_data["polls"] = {}
    
    context.bot_data["polls"][poll_number] = context.user_data["poll"]

    print("Created poll number: {}".format(str(poll_number)))

    share_button = InlineKeyboardButton(text='Share', switch_inline_query=str(poll_number)+" "+poll_question_text)
    share_menu = build_menu(button_list, n_cols = 1, header_buttons = [share_button], footer_buttons = None)
    context.bot.send_message(text = poll_text,
                            chat_id = chatid,
                            parse_mode=ParseMode.HTML,
                            reply_markup = InlineKeyboardMarkup(share_menu)
                            )
                            
    return 

def poll_inline_query_handler(update, context):

    print(update.inline_query.query)

    # inline query is <poll-number> <poll-question>
    # take poll number (split on first occurence of " " and take first element)
    poll_number = int(update.inline_query.query.split(" ", 1)[0])

    # Get the poll question linked to this poll number
    poll_question_text = context.bot_data["polls"][poll_number]["question"]

    # Get every poll option out as a list
    poll_options_list = list(context.bot_data["polls"][poll_number]["choices"].keys())

    # Gather the question and options into nice format
    poll_text = "<b>" + poll_question_text + "</b>"

    # For loop to go through every option in the options list in order to add the option text and names
    for option in poll_options_list:
        poll_text += "\n\n<b>" + option + ":</b>"
    
        option_name_list = context.bot_data["polls"][poll_number]["choices"][option]

        # insert all the current names below!
        for name in option_name_list:
            poll_text += "\n" + name 

    # Then reuse the menu object stored
    menu = context.bot_data["polls"][poll_number]["menu"]

    print(context.bot_data)

    inline_query_result = [
        InlineQueryResultArticle(
            id=poll_number, 
            title=poll_question_text, 
            input_message_content=
                InputTextMessageContent(
                    poll_text,
                    parse_mode=ParseMode.HTML
                ),
            reply_markup=InlineKeyboardMarkup(menu)
            )
        ]

    update.inline_query.answer(inline_query_result)

def update_poll(update, context):
    user = update.callback_query.from_user
    data_received = update.callback_query.data

    # callback data is <poll-id>_<option-text>. Split on first occurence of "_".
    processed_data_list = data_received.split("_", 1) 

    # Get the option pressed 
    option_pressed = processed_data_list[1]

    # Get the associated poll number for this button pressed 
    poll_number = int(processed_data_list[0])
    print("Updating poll number: {}".format(str(poll_number)))
    
    # Get the poll question linked to this poll number
    poll_question_text = context.bot_data["polls"][poll_number]["question"]

    # Get every poll option out as a list
    poll_options_list = list(context.bot_data["polls"][poll_number]["choices"].keys())

    # Update the info store with the name of the user who pressed this option
    name = user.first_name
    current_names_list = context.bot_data["polls"][poll_number]["choices"][option_pressed]
    if name in current_names_list:
        current_names_list.remove(name)
    else:
        current_names_list.append(name)
    context.bot_data["polls"][poll_number]["choices"][option_pressed] = current_names_list
    
    # Gather the question and options into nice format
    poll_text = "<b>" + poll_question_text + "</b>"

    # For loop to go through every option in the options list in order to add the option text and names
    for option in poll_options_list:
        poll_text += "\n\n<b>" + option + ":</b>"
    
        option_name_list = context.bot_data["polls"][poll_number]["choices"][option]

        # insert all the current names below!
        for name in option_name_list:
            poll_text += "\n" + name 

    # Then reuse the menu object stored
    menu = context.bot_data["polls"][poll_number]["menu"]

    print(context.bot_data)

    update.callback_query.edit_message_text(text = poll_text,
                                parse_mode=ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menu), # Add a reply markup to include the buttons!
                                ) 
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

    dispatcher.add_handler(InlineQueryHandler(poll_inline_query_handler))

    # Callback handler to handle data sent when anyone presses a button for an option
    dispatcher.add_handler(CallbackQueryHandler(callback = update_poll))

    dispatcher.add_error_handler(error)


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
