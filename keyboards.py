from aiogram.types import ReplyKeyboardRemove, \
    InlineKeyboardButton, InlineKeyboardMarkup

# TODO: Сделать в классы


# Шаг 1. Открыть проект или Загрузить новый проект
inline_btn_open = InlineKeyboardButton('Открыть', callback_data='open')
inline_kb_open = InlineKeyboardMarkup().add(inline_btn_open)
inline_btn_load = InlineKeyboardButton('Загрузить', callback_data='load')
inline_kb_load = InlineKeyboardMarkup().add(inline_btn_load)