from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    BOT_TOKEN: str = None
    REDIS_HOST: str = None

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    @staticmethod
    def get_commands():
        return [
            ("menu", "Главное меню"),
            ("cancel", "Отмена"),
        ]

