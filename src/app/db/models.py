from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index, func
from datetime import datetime

from app.db import Base


class SQLStorageRecord(Base):
    __tablename__ = "fsm_state_data"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[str|None]
    data: Mapped[dict|None]


class Warn(Base):
    __tablename__ = "warns"

    user_id: Mapped[int]
    chat_id: Mapped[int]
    reason: Mapped[str|None]

    warned_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        Index('warn_idx','chat_id','user_id'),
    )
    __mapper_args__ = {
        "primary_key": 'warned_at'
    }
