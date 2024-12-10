from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from filter.user_state import FSMBotState

from lexicon.lexicon import LEXICON_RU

router = Router()

@router.message(~StateFilter(FSMBotState.handle_file_state))
async def handle_other_message(message: Message):
    await message.answer(LEXICON_RU["other_message"])