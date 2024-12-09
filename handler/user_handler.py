from aiogram import F, Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command

from lexicon.lexicon import LEXICON_RU
from service.analyse_service import save_result_file

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

@router.message(F.document)
async def help_message_handler(message: Message, bot: Bot):

    local_path = './files_in/file_' + message.document.file_id + '.xslx'

    await bot.download(message.document.file_id, local_path)
    
    file_path = save_result_file(local_path, message.document.file_id)
    
    file = FSInputFile(file_path, filename="result.xlsx")

    await message.answer_document(document=file)