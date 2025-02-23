import asyncio

from moderator_project.adapters.bot.bot_starter import starter
from moderator_project.adapters.bot.settings import BotSettings
from moderator_project.aplication.configs.anomaly.service import AnomalyConfigService


bot_settings = BotSettings()


class Servises:
    anomaly_ervice = AnomalyConfigService()


if __name__ == '__main__':
    try:
        asyncio.run(
            starter(
                bot_settings.BOT_TOKEN,
                redis_host=bot_settings.REDIS_HOST,
                bot_commands=bot_settings.get_commands(),
                anomaly_ervice=Servises.anomaly_ervice,
            )
        )
    except (KeyboardInterrupt,):
        print('Bot stoped')