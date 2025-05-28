import asyncio

from moderator_project.adapters.bot.bot_starter import starter
from moderator_project.adapters.bot.settings import BotSettings
from moderator_project.aplication.configs.anomaly.service import AnomalyConfigService
from moderator_project.aplication.configs.trader.service import TraderPlusServise

bot_settings = BotSettings()


class Servises:
    anomaly_ervice = AnomalyConfigService()
    trader_ervice = TraderPlusServise()


if __name__ == '__main__':
    try:
        asyncio.run(
            starter(
                bot_settings.BOT_TOKEN,
                bot_commands=bot_settings.get_commands(),
                anomaly_ervice=Servises.anomaly_ervice,
                trader_ervice=Servises.trader_ervice,
            )
        )
    except (KeyboardInterrupt,):
        print('Bot stoped')