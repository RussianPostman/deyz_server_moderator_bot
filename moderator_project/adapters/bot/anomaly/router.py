from aiogram import Router, F
from aiogram.fsm.state import any_state

from moderator_project.adapters.bot.anomaly.handlers import add_anomaly_vait_file, add_anomaly_return_file
from moderator_project.adapters.bot.anomaly.states import AddAnomalyState


def register_anomaly_config_handler(router: Router):
    """
    Зарегистрировать хендлеры пользователя
    """

    router.message.register(
        add_anomaly_vait_file, F.text == 'Обновить конфиг аномалий', any_state
    )
    router.message.register(add_anomaly_return_file, AddAnomalyState.vait_file)
