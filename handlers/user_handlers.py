from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from lexicon.lexicon import ru_lexicon

router = Router()

@router.message(CommandStart())
async def processs_start_command(message: Message) -> None:
    await message.answer(text=ru_lexicon['/start'])