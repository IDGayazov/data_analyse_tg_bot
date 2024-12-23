from aiogram import F, Router, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from lexicon.lexicon import LEXICON_RU
from filter.user_state import FSMBotState
from filter.file_filter import XlsxFileFilter
from service.analyse_service import save_result_file, get_columns, missing_values_file_save, get_stat_file_save, get_outliers_file_save, get_values_file_save
from service.package_service import get_in_file_path, delete_files
from keyboard.keyboard import create_pagination_keyboard, create_keyboard
from database.database import user_dict_template, users_db


router = Router()

@router.message(CommandStart(), StateFilter(default_state))
async def start_message_handler(message: Message):
    await message.answer(text=LEXICON_RU['/start'])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = user_dict_template


@router.message(Command(commands='help'), StateFilter(default_state))
async def help_message_handler(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(Command(commands='fullan'), StateFilter(default_state))
async def fullan_message_handler(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/fullan'])
    await state.set_state(FSMBotState.handle_file_state)


@router.message(F.document, XlsxFileFilter(), StateFilter(FSMBotState.handle_file_state))
async def file_message_handler(message: Message, bot: Bot, state: FSMContext):
    in_file_path = get_in_file_path(message.document.file_id)
    await bot.download(message.document.file_id, in_file_path)
    out_file_path = save_result_file(in_file_path, message.document.file_id)

    file = FSInputFile(out_file_path, filename="result.xlsx")
    await message.answer_document(document=file)
    await state.set_state(default_state)
    delete_files()


@router.message(Command(commands='partan'), StateFilter(default_state))
async def fullan_message_handler(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/partan'])
    await state.set_state(FSMBotState.handle_partan_state)


@router.message(F.document, XlsxFileFilter(), StateFilter(FSMBotState.handle_partan_state))
async def file_message_handler(message: Message, bot: Bot, state: FSMContext):

    in_file_path = get_in_file_path(message.document.file_id)
    await bot.download(message.document.file_id, in_file_path)
    users_db[message.from_user.id]['file'] = message.document.file_id
    users_db[message.from_user.id]['path'] = in_file_path
    users_db[message.from_user.id]['columns'] = get_columns(in_file_path)
    users_db[message.from_user.id]['size'] = len(users_db[message.from_user.id]['columns'])
    users_db[message.from_user.id]['current_column'] = 0

    await message.answer(
        text=LEXICON_RU['choose_column'],
        reply_markup=create_pagination_keyboard(
            'backward',
            users_db[message.from_user.id]['columns'][users_db[message.from_user.id]['current_column']],
            'forward'
        )
    )


@router.callback_query(F.data == 'forward', StateFilter(FSMBotState.handle_partan_state))
async def process_forward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['current_column'] < users_db[callback.from_user.id]['size']:
        users_db[callback.from_user.id]['current_column'] += 1
        await callback.message.edit_text(
            text=LEXICON_RU['choose_column'],
            reply_markup=create_pagination_keyboard(
                'backward',
                users_db[callback.from_user.id]['columns'][users_db[callback.from_user.id]['current_column']],
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(F.data == 'backward', StateFilter(FSMBotState.handle_partan_state))
async def process_forward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['current_column'] > 0:
        users_db[callback.from_user.id]['current_column'] -= 1
        await callback.message.edit_text(
            text=LEXICON_RU['choose_column'],
            reply_markup=create_pagination_keyboard(
                'backward',
                users_db[callback.from_user.id]['columns'][users_db[callback.from_user.id]['current_column']],
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(F.data == 'missing_values', StateFilter(FSMBotState.handle_partan_state))
async def process_miss_value_press(callback_query: CallbackQuery, state: FSMContext):

    column = users_db[callback_query.from_user.id]['columns'][users_db[callback_query.from_user.id]['current_column']]
    out_file_path = missing_values_file_save(column, 
                                             users_db[callback_query.from_user.id]['file_id'],
                                             users_db[callback_query.from_user.id]['path'])

    file = FSInputFile(out_file_path, filename="result.xlsx")
    await callback_query.message.answer_document(document=file)
    await state.set_state(default_state)
    delete_files()

    await callback_query.answer()


@router.callback_query(F.data == 'get_stat', StateFilter(FSMBotState.handle_partan_state))
async def process_get_stat_press(callback_query: CallbackQuery, state: FSMContext):
    column = users_db[callback_query.from_user.id]['columns'][users_db[callback_query.from_user.id]['current_column']]
    out_file_path = get_stat_file_save(column, 
                                       users_db[callback_query.from_user.id]['file_id'], 
                                       users_db[callback_query.from_user.id]['path'])

    file = FSInputFile(out_file_path, filename="result.xlsx")
    await callback_query.message.answer_document(document=file)
    await state.set_state(default_state)
    delete_files()
    
    await callback_query.answer()


@router.callback_query(F.data == 'get_outliers', StateFilter(FSMBotState.handle_partan_state))
async def process_get_stat_press(callback_query: CallbackQuery, state: FSMContext):
    column = users_db[callback_query.from_user.id]['columns'][users_db[callback_query.from_user.id]['current_column']]
    out_file_path = get_outliers_file_save(column, 
                                       users_db[callback_query.from_user.id]['file_id'], 
                                       users_db[callback_query.from_user.id]['path'])

    file = FSInputFile(out_file_path, filename="result.xlsx")
    await callback_query.message.answer_document(document=file)
    await state.set_state(default_state)
    delete_files()

    await callback_query.answer()


@router.callback_query(F.data == 'get_values', StateFilter(FSMBotState.handle_partan_state))
async def process_get_stat_press(callback_query: CallbackQuery, state: FSMContext):
    column = users_db[callback_query.from_user.id]['columns'][users_db[callback_query.from_user.id]['current_column']]
    out_file_path = get_values_file_save(column, 
                                       users_db[callback_query.from_user.id]['file_id'], 
                                       users_db[callback_query.from_user.id]['path'])

    file = FSInputFile(out_file_path, filename="result.xlsx")
    await callback_query.message.answer_document(document=file)
    await state.set_state(default_state)
    delete_files()

    await callback_query.answer()


@router.callback_query(StateFilter(FSMBotState.handle_partan_state))
async def process_column_press(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text=LEXICON_RU['choose_action'],
        reply_markup=create_keyboard()
    )
    await callback_query.answer()


@router.message(StateFilter(FSMBotState.handle_file_state, FSMBotState.handle_partan_state))
async def error_file_message_handler(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['error_file'])