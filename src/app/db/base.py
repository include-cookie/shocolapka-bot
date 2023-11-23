from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import JSON

from app.config import DB_URL, DEBUG


Base = declarative_base(
    type_annotation_map={dict:JSON}
)

engine = create_async_engine(DB_URL, echo=DEBUG)

Session = async_sessionmaker(engine, expire_on_commit=False)

async def init_models():
    from app.db import models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
