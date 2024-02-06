from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import URLInputFile, Message, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.keyboard import parametersKeyboard, studentKeyboard, teacherKeyboard, noneKeyboard
from keyboards.inline_keyboard import accountDeleteKeyboard
from lexicon.lexicon import ru_processes_lexicon
from states.user_states import FSMSendMessage
from db import BotDB

router = Router()
schedule = URLInputFile('https://baksosh1.02edu.ru/upload/medialibrary/33b/o5ut7kic2o2hy98zhfgnehldo4rrh2l3/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%BD%D0%B0%203%20%D1%87%D0%B5%D1%82%D0%B2%D0%B5%D1%80%D1%82%D1%8C.pdf',
                     filename='Расписание.pdf')
database = BotDB('tgbot.db')
storage = MemoryStorage()
user_dict = {}


# Отправка расписания
@router.message(F.text == 'Расписание')
async def schedule_send(message: Message) -> None:
    await message.answer(text=ru_processes_lexicon['scheduleSent'])
    await message.answer_document(schedule)

# Отправка сообщения какому-то классу
@router.message(F.text == 'Отправить сообщение')
async def send_message(message: Message, state: FSMContext):
    if database.teacher_exists(message.from_user.id):
        await message.answer(text=ru_processes_lexicon['sendMessage'])
        await state.set_state(FSMSendMessage.fill_text)

# Этот хендлер сохраняет текст сообщения и переводит машину в состояние ввода класса
@router.message(StateFilter(FSMSendMessage.fill_text))
async def process_text_sent(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    user_dict['text'] = message.text
    await message.answer(text=ru_processes_lexicon['sendGrade'])
    await state.set_state(FSMSendMessage.fill_grade)

# Этот хендлер отправляет сообщение и завершает машину состояний
@router.message(StateFilter(FSMSendMessage.fill_grade))
async def process_grade_sent(message: Message, bot: Bot, state: FSMContext):
    await message.answer(text='sdsd')
    await state.update_data(grade=message.text)
    user_dict['grade'] = message.text
    users = database.select_id_to_send_message(user_dict['grade'])
    for i in range(len(users)):
        for j in users[i]:
            await bot.send_message(int(j), user_dict['text'])
    await message.answer(ru_processes_lexicon['messageSent'])
    await state.clear()

# Переход в клавиатуру параметров
@router.message(F.text == 'Параметры')
async def parameters_keyboard(message: Message) -> None:
    await message.answer(text=message.text, reply_markup=parametersKeyboard)

# Отправка данных пользователю
@router.message(F.text == 'Мои данные')
async def my_data(message: Message):
    await message.answer(text=database.show_data(message.from_user.id))

# Удаление учетной записи пользователя
@router.message(F.text == 'Удалить учетную запись')
async def account_delete_warning(message: Message):
    await message.answer(text=ru_processes_lexicon['accountDeleteWarning'], reply_markup=accountDeleteKeyboard)

@router.callback_query(F.data.in_(['yes','no']))
async def account_delete(callback: CallbackQuery):
    if (callback.data == 'yes'):
        database.delete_user(callback.message.from_user.id)
        await callback.message.delete()
        await callback.message.answer(text=ru_processes_lexicon['accountDeleted'], reply_markup=noneKeyboard)
    else:
        await callback.message.delete()
        await callback.message.answer(text=ru_processes_lexicon['accountDeleteCanceled'])

# Сворачивание клавиатуры параметров
@router.message(F.text == 'Назад')
async def exit_parameters_keyboard(message: Message):
    if database.student_exists(message.from_user.id):
        await message.answer(text=message.text, reply_markup=studentKeyboard)
    else:
        await message.answer(text=message.text, reply_markup=teacherKeyboard)