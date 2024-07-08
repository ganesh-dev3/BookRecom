from config import *
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager

#DATABASE_URL = 'sqlite+aiosqlite:///booksnew.db'
#DATABASE_URL = 'postgresql+asyncpg://<db_username>:<db_secret>@<db_host>:<db_port>/<db_name>'
DATABASE_URL = 'postgresql+asyncpg://%s:%s@%s:%s/%s'%(db_uname, db_passwd, db_host, db_port, db_name)

engine = create_async_engine(DATABASE_URL, future=True, echo=True)

@asynccontextmanager
async def get_session():
    async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session

Base = declarative_base()



