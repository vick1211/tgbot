from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, URLInputFile
from lexicon.lexicon import ru_commands_lexicon, ru_processes_lexicon
from keyboards.keyboard import my_keyboard
from db import BotDB

router = Router()
database = BotDB('tgbot.db')
schedule = URLInputFile('https://baksosh1.02edu.ru/upload/medialibrary/2d6/e5k19m68az0wu3807o0apy80tidtxyid/WhatsApp%20Image%202023-11-20%20at%2013.10.23.pdf',
                     filename='second-quarter-schedule.pdf')
user_dict = {}
storage = MemoryStorage()

class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_post = State()
    fill_grade = State()

#Обработка команды /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    studentData = database.student_exists(message.from_user.id)
    if studentData:
        await message.answer(text=ru_processes_lexicon['alreadyRegistered'], reply_markup=my_keyboard)
    else:
        teacherData = database.teacher_exists(message.from_user.id)
        if teacherData:
            await message.answer(text=ru_processes_lexicon['alreadyRegistered'], reply_markup=my_keyboard)
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
    studentButton = InlineKeyboardButton(text='Ученик', callback_data='student')
    teacherButton = InlineKeyboardButton(text='Учитель', callback_data='teacher')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[studentButton],[teacherButton]])
    await message.answer(text='Теперь выберите должность', reply_markup=keyboard)
    await state.set_state(FSMFillForm.fill_post)

# Этот хендлер
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
        database.add_teacher(callback.message.from_user.id ,user_dict['name'])
        await state.clear()
        await callback.message.answer(text='Регистрация прошла успешно. Если хотите посмотреть свои данные, введите команду /showdata',reply_markup=my_keyboard)

@router.message(StateFilter(FSMFillForm.fill_grade))
async def process_grade_sent(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_dict['grade'] = message.text
    database.add_student(message.from_user.id ,user_dict['name'], user_dict['grade'])
    await state.clear()
    await message.answer('Регистрация прошла успешно. Если хотите посмотреть свои данные, введите команду /showdata')

@router.message(Command(commands='showdata'))
async def process_showdata_command(message: Message):
    await message.answer(text=database.showdata(message.from_user.id))

@router.message(Command('help'))
async def process_help_command(message: Message) -> None:
     await message.answer(text=ru_commands_lexicon['/help'])

@router.message(F.text == 'Расписание')
async def schedule_send(message: Message) -> None:
    await message.answer_document(schedule)
