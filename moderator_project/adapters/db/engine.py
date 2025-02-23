# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
#
# engine = create_async_engine("sqlite+aiosqlite:///tasks.db")
# new_session = async_sessionmaker(engine, expire_on_commit=False)
#

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine


def create_async_engine(url: str) -> AsyncEngine:
    return _create_async_engine(
        url=url,
        echo=True,
        #  encoding='utf-8',
        pool_pre_ping=True
    )


def get_session_maker(engine: AsyncEngine) -> AsyncSession:
    return async_sessionmaker(engine, expire_on_commit=False)
