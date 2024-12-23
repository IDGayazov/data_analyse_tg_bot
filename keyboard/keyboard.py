from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_KEYBOARD, LEXICON_RU


def create_pagination_keyboard(*buttons):
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON_KEYBOARD[button] if button in LEXICON_KEYBOARD else button,
        callback_data=button) for button in buttons]
    )
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

def create_keyboard():
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['missing_values'],
            callback_data='missing_values'
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['get_stat'],
            callback_data='get_stat'
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['get_outliers'],
            callback_data='get_outliers'
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['get_values'],
            callback_data='get_values'
        ),
        width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()