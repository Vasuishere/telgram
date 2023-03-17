import logging
from Inline_Keyboard_Creator import Inline_Keyboard_Maker,DirectoryName_Pattern
from UserDatabase_Register import is_user_registered,register_user,get_user_branch
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
from functools import partial
import os
from telegram import InputFile
import json


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

Global_dynamic_paths=''
with open('config.json', 'r') as f:
    config = json.load(f)

token = config['bot_token']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if is_user_registered(chat_id=update.message.chat.id):
        await subject_flow(update,context,context.application)
    else :
        keyboard = [
            [
                InlineKeyboardButton("Register!", callback_data="register"),
                InlineKeyboardButton("Help!", callback_data="help"),
            ],
            [InlineKeyboardButton("Others", callback_data="others")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def register(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    dynamic_path = "Branch"
    reply_markup = Inline_Keyboard_Maker(dynamic_path,row_count=3)
    await query.answer()
    await query.edit_message_text(text="Please choose your branch:", reply_markup=reply_markup)

async def register_branch(update: Update, context: CallbackContext) -> None:
    print("register block active!")
    query = update.callback_query
    branch=query.data
    username = query.from_user.first_name
    chat_id = query.message.chat.id
    keyboard = [
        [
            InlineKeyboardButton("Continue!", callback_data="continue"),
            InlineKeyboardButton("Help!", callback_data="help"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    registration_status=register_user(chat_id, branch, username)
    await query.answer()
    await query.edit_message_text(text=registration_status,reply_markup=reply_markup)

async def subject_flow(update: Update, context:CallbackContext, application: Application) -> None:
    global Global_dynamic_paths
    print("Subject flow initiated !")
    query = update.callback_query
    if query is not None and query.message is not None:
        Global_dynamic_paths = f"Branch/{get_user_branch(query.message.chat.id)}"
        print(Global_dynamic_paths)
        await query.answer()
        await query.edit_message_text(text="Choose your subject!", reply_markup=Inline_Keyboard_Maker(Global_dynamic_paths, row_count=2))
    else:
        print("else block of subject flow!")
        Global_dynamic_paths = f"Branch/{get_user_branch(update.message.from_user.id)}"
        print(Global_dynamic_paths)
        await update.message.reply_text(text="Which Subject Assignment Do You Want!", reply_markup=Inline_Keyboard_Maker(Global_dynamic_paths, row_count=2))
    application.add_handler(CallbackQueryHandler(partial(file_flow, application=application), pattern=DirectoryName_Pattern(Global_dynamic_paths)))

async def file_flow(update:Update, context:CallbackContext, application: Application) -> None:
    print("file flow initiated !")
    query= update.callback_query
    global Global_dynamic_paths
    dynamic_path=os.path.join(Global_dynamic_paths,query.data)
    await query.answer()
    await query.edit_message_text(text="Choose a file to download!!", reply_markup=Inline_Keyboard_Maker(dynamic_path, row_count=2, back_path="continue"))
    Global_dynamic_paths=dynamic_path
    application.add_handler(CallbackQueryHandler(partial(final_file_download_flow, application=application), pattern=DirectoryName_Pattern(Global_dynamic_paths)))

async def final_file_download_flow(update: Update, context: CallbackContext, application: Application):
    print("final flow initiated!")
    query = update.callback_query
    global Global_dynamic_paths
    file_path = os.path.join(Global_dynamic_paths,query.data)
    print(file_path)

    with open(file_path, "rb") as f:
        file_name = os.path.basename(file_path)
        await query.answer()
        await query.delete_message()
        await context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(f, filename=file_name))
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose a file to download!", reply_markup=Inline_Keyboard_Maker(Global_dynamic_paths, row_count=2, back_path="continue"))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text("Use /start to test this bot.\n For other help contact us on xxx.gamil.com!")

def main() -> None:

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(register,pattern='register'))
    application.add_handler(CallbackQueryHandler(register_branch,pattern=DirectoryName_Pattern("Branch")))
    application.add_handler(CallbackQueryHandler(partial(subject_flow,application=application),pattern='continue'))
    application.add_handler(CallbackQueryHandler(help_command, pattern='help'))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling(poll_interval=2.0,pool_timeout=40)
