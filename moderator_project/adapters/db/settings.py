from urllib.parse import quote

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_NAME: str = 'postgres'
    DATABASE_HOST: str = 'localhost'
    DATABASE_PORT: int = None
    DATABASE_USER: str = 'postgres'
    DATABASE_PASS: str = quote('password')

    ALEMBIC_MIGRATION_FILENAME_TEMPLATE: str = (
        '%%(year)d_'
        '%%(month).2d_'
        '%%(day).2d_'
        '%%(hour).2d_'
        '%%(minute).2d_'
        '%%(second).2d_'
        '%%(slug)s'
    )

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    @property
    def DATABASE_URL(self):
        url = 'postgresql+asyncpg://{db_user}:{db_pass}@{db_host}'\
              ':{db_port}/{db_name}'

        return url.format(
            db_user=self.DATABASE_USER,
            db_pass=self.DATABASE_PASS,
            db_host=self.DATABASE_HOST,
            db_name=self.DATABASE_NAME,
            db_port=self.DATABASE_PORT,
        )
