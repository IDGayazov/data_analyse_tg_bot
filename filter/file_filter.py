from aiogram.filters import BaseFilter
from aiogram.types import Message

from lexicon.lexicon import LEXICON_RU

class XlsxFileFilter(BaseFilter):
    
    async def __call__(self, message: Message) -> bool:
        extension = message.document.file_name.split(".")[-1]

        if extension != 'xlsx':
            return False
        else:
            return True