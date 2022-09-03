from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛍 Mahsulotlar"),
        ],
        [
        KeyboardButton(text="🛒 Savatcha"),
        KeyboardButton(text='Ko\'proq...'),
        ],
    ],
    resize_keyboard=True,
)

menu_2=ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="1"),
        KeyboardButton(text="2"),
        KeyboardButton(text="3"),
    ],
        [
        KeyboardButton(text="4"),
        KeyboardButton(text="5"),
        KeyboardButton(text="6"),
    ],
        [
        KeyboardButton(text="7"),
        KeyboardButton(text="8"),
        KeyboardButton(text="9"),
    ],
        [
        KeyboardButton(text="⬅️Ortga"),
    ],
        ],
    resize_keyboard=True,
)
