from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage

from moderator_project.adapters.bot.base.keyboards import MENU_BOARD


async def start(message: types.Message):

    return await message.answer(
        text='Добро пожаловать',
        # chat_id=message.from_user.id,
        reply_markup=MENU_BOARD
    )


# функция выхода из машины состояний
async def censel_hendler(
    message: types.Message,
    state: FSMContext,
    bot: Bot,
):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await bot.send_message(
        text='Дейстаия отменены',
        chat_id=message.from_user.id,
        reply_markup=MENU_BOARD
    )