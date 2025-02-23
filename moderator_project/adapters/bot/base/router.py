__all__ = ['register_user_commands']

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import any_state

from moderator_project.adapters.bot.base.handlers import start, censel_hendler


def register_base_handler(router: Router):
    """
    Зарегистрировать хендлеры пользователя
    """
    router.message.register(start, CommandStart())
    router.message.register(start, Command('menu'))

    router.message.register(censel_hendler, Command('cancel'), any_state)
    router.message.register(censel_hendler, Command('menu'), any_state)
    router.message.register(censel_hendler, F.text.casefold().lower() == 'отмена', any_state)
    router.callback_query.register(censel_hendler, F.data == 'cancel', any_state)