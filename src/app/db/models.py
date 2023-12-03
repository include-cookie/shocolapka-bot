from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index, func
from datetime import datetime

from app.db import Base


class SQLStorageRecord(Base):
    __tablename__ = "fsm_state_data"

    chat_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[str|None]
    data: Mapped[dict|None]


class Warn(Base):
    __tablename__ = "warns"

    chat_id: Mapped[int]
    user_id: Mapped[int]
    reason: Mapped[str|None]

    warned_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        Index('warns_idx','chat_id','user_id'),
    )
    __mapper_args__ = {
        "primary_key": 'warned_at'
    }

class Dialog(Base):
    __tablename__ = "dialogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    peer_id: Mapped[int] = mapped_column(index=True)
