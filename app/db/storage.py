from aiogram.fsm.state import State
from aiogram.fsm.storage.base import (
    BaseStorage,
    StateType,
    StorageKey
)

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from app.db import Session
from app.db.models import SQLStorageRecord


class SQLStorage(BaseStorage):

    def __init__(self):
        self.session = Session()

    async def close(self):
        await self.session.close()

    async def set_state(self, key: StorageKey, state: StateType = None):
        stmt = insert(SQLStorageRecord).values(
            user_id=key.user_id,
            chat_id=key.chat_id,
            state=state.state if isinstance(state, State) else state
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[SQLStorageRecord.user_id,SQLStorageRecord.chat_id],
            set_=dict(state=stmt.excluded.state)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_state(self, key: StorageKey):
        return (
            await self.session.scalar(
                select(SQLStorageRecord.state).
                where(
                    SQLStorageRecord.user_id == key.user_id,
                    SQLStorageRecord.chat_id == key.chat_id
                )
            )
        )

    async def set_data(self, key: StorageKey, data: dict):
        stmt = insert(SQLStorageRecord).values(
            user_id=key.user_id,
            chat_id=key.chat_id,
            data=data
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[SQLStorageRecord.user_id,SQLStorageRecord.chat_id],
            set_=dict(data=stmt.excluded.data)
        )
        await self.session.execute(stmt)
        await self.session.commit()


    async def get_data(self, key: StorageKey) -> dict:
        return (
            await self.session.scalar(
                select(SQLStorageRecord.data).
                where(
                    SQLStorageRecord.user_id == key.user_id,
                    SQLStorageRecord.chat_id == key.chat_id
                )
            )
        )
