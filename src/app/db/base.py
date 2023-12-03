from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import BIGINT

from app.config import DB_URL, DEBUG


Base = declarative_base(
    type_annotation_map={dict:JSONB,int:BIGINT}
)

engine = create_async_engine(DB_URL, echo=DEBUG)

Session = async_sessionmaker(engine, expire_on_commit=False)
