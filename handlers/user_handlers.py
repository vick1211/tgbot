from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import ru_commands_lexicon, ru_processes_lexicon
from keyboards.keyboard import studentKeyboard, teacherKeyboard
from keyboards.inline_keyboard import regKeyboard,helpKeyboard
from states.user_states import FSMFillForm
from db import BotDB

router = Router()
database = BotDB('tgbot.db')
user_dict = {}
storage = MemoryStorage()

#Обработка команды /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    studentData = database.student_exists(message.from_user.id)
    if studentData:
        await message.answer(text=ru_processes_lexicon['alreadyRegistered'], reply_markup=studentKeyboard)
    else:
        teacherData = database.teacher_exists(message.from_user.id)
        if teacherData:
            await message.answer(text=ru_processes_lexicon['alreadyRegistered'], reply_markup=teacherKeyboard)
        else:
            await message.answer(text=ru_commands_lexicon['/start'])

# Обработка команды /fillform, запуск регистрации
@router.message(Command(commands='fillform'))
async def process_fillform_command(message: Message, state:FSMContext):
    await message.answer(text='Введите ваше имя')
    # Устанавливаем состояние ввода имени
    await state.set_state(FSMFillForm.fill_name)

# Этот хендлер переводит машину в состояние выбора должности
@router.message(StateFilter(FSMFillForm.fill_name))
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_dict['name'] = message.text
    await message.answer(text='Теперь выберите должность', reply_markup=regKeyboard)
    await state.set_state(FSMFillForm.fill_post)

# Этот хендлер переводит в состояние ввода класса либо завершает машину, в зависимости от введенных данных
@router.callback_query(StateFilter(FSMFillForm.fill_post), F.data.in_(['student', 'teacher']))
async def process_post_sent(callback: CallbackQuery, state: FSMContext):
    await state.update_data(post=callback.data)
    if (callback.data == 'student'):
        user_dict['post'] = 'Ученик'
        await callback.message.delete()
        await callback.message.answer('Теперь введите свой класс')
        await state.set_state(FSMFillForm.fill_grade)
    else:
        user_dict['post'] = 'Учитель'
        await callback.message.delete()
        database.add_teacher(callback.from_user.id ,user_dict['name'])
        await state.clear()
        await callback.message.answer(text=ru_processes_lexicon['regComplete'],reply_markup=teacherKeyboard)

# Этот хендлер завершает машину состояний
@router.message(StateFilter(FSMFillForm.fill_grade))
async def process_grade_sent(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_dict['grade'] = message.text
    database.add_student(message.from_user.id ,user_dict['name'], user_dict['grade'])
    await state.clear()
    await message.answer(text=ru_processes_lexicon['regComplete'], reply_markup=studentKeyboard)

# Обработка команды /showdata
@router.message(Command(commands='showdata'))
async def process_showdata_command(message: Message):
    await message.answer(text=database.show_data(message.from_user.id))

# Обработка команды /help
@router.message(Command('help'))
async def process_help_command(message: Message) -> None:
    await message.answer(text=ru_commands_lexicon['/help'], reply_markup=helpKeyboard)

# Этот хендлер выводит пользователю нужную помощь
@router.callback_query(F.data.in_(['checkCommands']))
async def process_checkCommands(callback: CallbackQuery):
    await callback.message.answer(text=ru_processes_lexicon['checkCommands'])