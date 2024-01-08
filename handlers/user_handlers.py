from aiogram import Router, F
from aiogram.types import Message, URLInputFile
from aiogram.filters import CommandStart, Command
from lexicon.lexicon import ru_lexicon
from keyboards.keyboard import my_keyboard

router = Router()
schedule = URLInputFile('https://baksosh1.02edu.ru/upload/medialibrary/2d6/e5k19m68az0wu3807o0apy80tidtxyid/WhatsApp%20Image%202023-11-20%20at%2013.10.23.pdf',
                     filename='second-quarter-schedule.pdf')

@router.message(CommandStart())
async def processs_start_command(message: Message) -> None:
    await message.answer(text=ru_lexicon['/start'], reply_markup=my_keyboard)

@router.message(Command('help'))
async def process_help_command(message: Message) -> None:
    await message.answer(text=ru_lexicon['/help'])

@router.message(F.text == 'Расписание')
async def schedule_send(message: Message) -> None:
    await message.answer_document(schedule)