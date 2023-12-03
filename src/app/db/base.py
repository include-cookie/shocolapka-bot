from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import BIGINT
from asyncio import current_task


from app.config import DB_URL, DEBUG


Base = declarative_base(
    type_annotation_map={dict:JSONB,int:BIGINT}
)

engine = create_async_engine(DB_URL, echo=DEBUG)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

AsyncScopedSession = async_scoped_session(async_session_factory,scopefunc=current_task)
