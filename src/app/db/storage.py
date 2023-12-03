from aiogram.fsm.state import State
from aiogram.fsm.storage.base import (
    BaseStorage,
    StateType,
    StorageKey
)

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.db import AsyncScopedSession
from app.db.models import SQLStorageRecord


class SQLStorage(BaseStorage):

    def __init__(self):
        self.session = AsyncScopedSession()

    async def close(self):
        await self.session.close()
        await AsyncScopedSession.remove()


    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        stmt = insert(SQLStorageRecord).values(
            chat_id=key.chat_id,
            user_id=key.user_id,
            state=state.state if isinstance(state, State) else state
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[SQLStorageRecord.chat_id,SQLStorageRecord.user_id],
            set_=dict(state=stmt.excluded.state)
        )
        await self.session.execute(stmt)
        await self.session.commit()


    async def get_state(self, key: StorageKey) -> str|None:
        return (
            await self.session.scalar(
                select(SQLStorageRecord.state).
                where(
                    SQLStorageRecord.chat_id == key.chat_id,
                    SQLStorageRecord.user_id == key.user_id,
                )
            )
        )


    async def set_data(self, key: StorageKey, data: dict) -> None:
        stmt = insert(SQLStorageRecord).values(
            chat_id=key.chat_id,
            user_id=key.user_id,
            data=data
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[SQLStorageRecord.chat_id,SQLStorageRecord.user_id],
            set_=dict(data=stmt.excluded.data)
        )
        await self.session.execute(stmt)
        await self.session.commit()


    async def get_data(self, key: StorageKey) -> dict:
        return (
            await self.session.scalar(
                select(SQLStorageRecord.data).
                where(
                    SQLStorageRecord.chat_id == key.chat_id,
                    SQLStorageRecord.user_id == key.user_id,
                )
            )
        )


def fix_storage_key(key: StorageKey) -> StorageKey:
    return StorageKey(
        bot_id=key.bot_id,
        chat_id=key.user_id,
        user_id=key.user_id,
        thread_id=key.thread_id,
        destiny=key.destiny,
    )
