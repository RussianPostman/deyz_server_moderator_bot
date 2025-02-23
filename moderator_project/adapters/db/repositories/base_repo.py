from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine


class BaseRepository:
    engine: AsyncEngine

    def __init__(self, url: str):
        self.engine = self._create_async_engine(url)

    @staticmethod
    def _create_async_engine(url: str) -> AsyncEngine:
        return _create_async_engine(
            url=url,
            echo=True,
            #  encoding='utf-8',
            pool_pre_ping=True
        )

    def get_session_maker(self) -> async_sessionmaker:
        return async_sessionmaker(self.engine, expire_on_commit=False)
