from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard: list[list[KeyboardButton]] = []

keyboard.append([KeyboardButton(text='Расписание')])

my_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)