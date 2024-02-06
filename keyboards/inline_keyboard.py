from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

studentButton = InlineKeyboardButton(text='Ученик', callback_data='student')
teacherButton = InlineKeyboardButton(text='Учитель', callback_data='teacher')

regKeyboard = InlineKeyboardMarkup(inline_keyboard=[[studentButton],
                                                    [teacherButton]])

checkCommandsButton = InlineKeyboardButton(text='Просмотреть доступные команды', callback_data='checkCommands')

helpKeyboard = InlineKeyboardMarkup(inline_keyboard=[[checkCommandsButton]])

deleteAccountButton = InlineKeyboardButton(text='Да', callback_data='yes')
notDeleteAccountButton = InlineKeyboardButton(text='Нет', callback_data = 'no')

accountDeleteKeyboard = InlineKeyboardMarkup(inline_keyboard=[[deleteAccountButton],
                                                              [notDeleteAccountButton]])