from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from lexicon.lexicon import ru_lexicon

router = Router()

@router.message(CommandStart())
async def processs_start_command(message: Message) -> None:
    await message.answer(text=ru_lexicon['/start'])

@router.message(Command('help'))
async def process_help_command(message: Message) -> None:
    await message.answer(text=ru_lexicon['/help'])