"""
Файл запуска бота
"""
import logging

from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from aioredis import Redis
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram import Bot, Dispatcher

from moderator_project.adapters.bot.anomaly.router import register_anomaly_config_handler
from moderator_project.adapters.bot.base.router import register_base_handler
from moderator_project.aplication.configs.anomaly.service import AnomalyConfigService


async def starter(
    token: str,
    bot_commands: list[tuple[str]],
    anomaly_ervice: AnomalyConfigService,
    redis_host: str = None,
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

    await bot.set_my_commands(commands=commands_for_bot)

    await dp.start_polling(bot, anomaly_ervice=anomaly_ervice)
