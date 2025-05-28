from aiogram import Router, F
from aiogram.fsm.state import any_state

from moderator_project.adapters.bot.trader_plus.handlers import add_trader_vait_file, add_trader_return_file
from moderator_project.adapters.bot.trader_plus.states import AddTraderState


def register_trader_config_handler(router: Router):
    """
    Зарегистрировать хендлеры для конфигов трейдера
    """

    router.message.register(
        add_trader_vait_file, F.text == 'Обновить конфиг трейдер+', any_state
    )
    router.message.register(add_trader_return_file, AddTraderState.vait_file)
