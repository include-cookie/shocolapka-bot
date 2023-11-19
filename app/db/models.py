from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class SQLStorageRecord(Base):
    __tablename__ = "fsm_state_data"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[Optional[str]]
    data: Mapped[Optional[dict]]
