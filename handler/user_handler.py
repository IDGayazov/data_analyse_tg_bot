from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from lexicon.lexicon import LEXICON_RU

router = Router()

@router.message(CommandStart())
async def start_message_handler(message: Message):
    await message.answer(text=LEXICON_RU['/start'])

@router.message(Command(commands='help'))
async def help_message_handler(message):
    await message.answer(text=LEXICON_RU['/help'])

@router.message(Command(commands='fullan'))
async def help_message_handler(message):
    await message.answer(text=LEXICON_RU['/fullan'])