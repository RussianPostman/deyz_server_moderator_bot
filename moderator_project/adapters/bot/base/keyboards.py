from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Обновить конфиг аномалий"),
        ],
        [
            KeyboardButton(text='Обновить конфиг трейдер+'),
        ],
    ],
    resize_keyboard=True
)
