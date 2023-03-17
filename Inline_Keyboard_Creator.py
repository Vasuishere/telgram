import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def Inline_Keyboard_Maker(path:str, row_count:int, back_path:str=None):
    directories = os.listdir(path)

    keyboard_buttons = [InlineKeyboardButton(text=d, callback_data=d) for d in directories]

    keyboard_rows = [keyboard_buttons[i:i+row_count] for i in range(0, len(keyboard_buttons), row_count)]

    if back_path:
        back_button = InlineKeyboardButton(text="Back", callback_data=back_path)
        keyboard_rows.append([back_button])

    keyboard = InlineKeyboardMarkup(keyboard_rows)
    return keyboard

def DirectoryName_Pattern(path):
    pattern = '^(' + '|'.join(os.listdir(path)) + ')$'
    return pattern
