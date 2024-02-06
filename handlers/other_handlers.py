from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from lexicon.lexicon import ru_commands_lexicon,ru_processes_lexicon

router = Router()

@router.message(Command(commands='delmenu'))
async def del_main_menu(message: Message, bot:Bot) -> None:
    await bot.delete_my_commands()
    await message.answer(text=ru_commands_lexicon['/delmenu'])

@router.message()
async def warning_not_declared_command(message: Message):
    await message.answer(text=ru_processes_lexicon['incorrectCommand'])