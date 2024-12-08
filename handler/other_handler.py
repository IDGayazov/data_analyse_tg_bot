from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon import LEXICON_RU

router = Router()

@router.message()
async def handle_other_message(message: Message):
    await message.answer(LEXICON_RU["other_message"])