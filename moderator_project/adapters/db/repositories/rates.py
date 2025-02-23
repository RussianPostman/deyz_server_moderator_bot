from datetime import datetime

from sqlalchemy import select, desc

from moderator_project.adapters.db.models import Rate
from moderator_project.adapters.db.repositories import BaseRepository
from moderator_project.aplication.rates.interfaces import RateInterface


class RateRepository(BaseRepository, RateInterface):

    async def get_rate(self, name: str, date: datetime) -> list[Rate]:
        async with self.get_session_maker()() as session:
            async with session.begin():
                sql_res = await session.execute(
                    select(Rate)
                    .where(
                        Rate.name == name,
                        Rate.date_to < date,
                    )
                    .order_by(desc(Rate.date_to))
                )
                return sql_res.first()
