from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import settings


# sync engine for db connection
sync_engine = create_engine(
    url=settings.db_url_psycopg,
    echo=True,
    pool_size=5,  # amount of connections
    max_overflow=10,  # amount of additional connections if pool_size is full
)

# async engine for db connection
async_engine = create_async_engine(
    url=settings.db_url_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

sync_session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)
