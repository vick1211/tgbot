from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard1: list[list[KeyboardButton]] = []

keyboard1.append([KeyboardButton(text='Расписание')])
keyboard1.append([KeyboardButton(text='Параметры')])

studentKeyboard = ReplyKeyboardMarkup(keyboard=keyboard1, resize_keyboard=True)

keyboard1.append([KeyboardButton(text='Отправить сообщение')])

teacherKeyboard = ReplyKeyboardMarkup(keyboard=keyboard1, resize_keyboard=True)

keyboard2: list[list[KeyboardButton]] = []

keyboard2.append([KeyboardButton(text='Мои данные')])
keyboard2.append([KeyboardButton(text='Удалить учетную запись')])
keyboard2.append([KeyboardButton(text='Назад')])

parametersKeyboard = ReplyKeyboardMarkup(keyboard=keyboard2, resize_keyboard=True)

keyboard3 = []

noneKeyboard = ReplyKeyboardMarkup(keyboard=keyboard3)