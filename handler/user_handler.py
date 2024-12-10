from aiogram import F, Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage


from lexicon.lexicon import LEXICON_RU
from filter.user_state import FSMBotState
from filter.file_filter import XlsxFileFilter
from service.analyse_service import save_result_file

router = Router()

@router.message(CommandStart(), StateFilter(default_state))
async def start_message_handler(message: Message):
    await message.answer(text=LEXICON_RU['/start'])

@router.message(Command(commands='help'), StateFilter(default_state))
async def help_message_handler(message: Message):
    await message.answer(text=LEXICON_RU['/help'])

@router.message(Command(commands='fullan'), StateFilter(default_state))
async def fullan_message_handler(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/fullan'])
    await state.set_state(FSMBotState.handle_file_state)

@router.message(F.document, XlsxFileFilter(), StateFilter(FSMBotState.handle_file_state))
async def file_message_handler(message: Message, bot: Bot, state: FSMContext):

    local_path = './files_in/file_' + message.document.file_id + '.xslx'

    await bot.download(message.document.file_id, local_path)
    
    file_path = save_result_file(local_path, message.document.file_id)
    
    file = FSInputFile(file_path, filename="result.xlsx")

    await message.answer_document(document=file)

    await state.set_state(default_state)

@router.message(StateFilter(FSMBotState.handle_file_state))
async def error_file_message_handler(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['error_file'])