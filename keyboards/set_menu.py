from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon import ru_menuCommands_lexicon

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in ru_menuCommands_lexicon.items()
    ]
    await bot.set_my_commands(main_menu_commands)