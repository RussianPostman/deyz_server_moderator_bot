from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Обновить конфиг аномалий"),
        ],
        # [
        #     KeyboardButton(text='Список сталкеров'),
        # ],
    ],
    resize_keyboard=True
)
