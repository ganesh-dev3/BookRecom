from config import *
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager

DATABASE_URL = 'sqlite+aiosqlite:///booksnew.db'

engine = create_async_engine(DATABASE_URL, future=True, echo=True)

@asynccontextmanager
async def get_session():
    async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session

Base = declarative_base()



