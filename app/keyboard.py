from aiogram.types import InlineKeyboardMarkup, KeyboardButton


markup = InlineKeyboardMarkup()
markup.add(
    KeyboardButton(text="Выполнено", callback_data="done_true"),
    KeyboardButton(text="Не сделано", callback_data="done_false")
)
