from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from moderator_project.adapters.db.models import BaseModel


class Config(BaseModel):
    __tablename__ = 'config'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    description: Mapped[str]
    config = Column(JSONB)


class Detector(BaseModel):
    __tablename__ = 'detector'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    class_name: Mapped[str]
    radius: Mapped[int]
