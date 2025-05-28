"""
Файл запуска бота
"""
import logging

from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram import Bot, Dispatcher

from moderator_project.adapters.bot.anomaly.router import register_anomaly_config_handler
from moderator_project.adapters.bot.base.router import register_base_handler
from moderator_project.adapters.bot.trader_plus.router import register_trader_config_handler
from moderator_project.aplication.configs.anomaly.service import AnomalyConfigService
from moderator_project.aplication.configs.trader.service import TraderPlusServise


async def starter(
    token: str,
    bot_commands: list[tuple[str]],
    anomaly_ervice: AnomalyConfigService,
    trader_ervice: TraderPlusServise,
):
    logging.basicConfig(level=logging.DEBUG)

    # redis = Redis(host=redis_host)
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token)

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    register_base_handler(dp)
    register_anomaly_config_handler(dp)
    register_trader_config_handler(dp)

    await bot.set_my_commands(commands=commands_for_bot)

    await dp.start_polling(
        bot, anomaly_ervice=anomaly_ervice, trader_ervice=trader_ervice,
    )
