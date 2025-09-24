from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from config import DATABASES
import logging

logger = logging.getLogger(__name__)

def get_connection_string(db_key: str) -> str:
    """
    Constructs the database connection string for SQLAlchemy
    """
    try:
        db = DATABASES[db_key]
        driver = db["driver"].replace(" ", "+")
        return f"{db['type']}://{db['username']}:{db['password']}@{db['server']}/{db['database']}?driver={driver}"
    except KeyError as e:
        logger.error(f"Database configuration not found for key: {db_key}")
        raise ValueError(f"Invalid database key: {db_key}") from e

def create_engine_and_session(db_key: str):
    """
    Creates and returns a SQLAlchemy async engine and sessionmaker
    for a given database key from config.
    """
    connection_string = get_connection_string(db_key)
    
    engine = create_async_engine(
        connection_string,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=False  # Set to True for SQL query logging in development
    )
    
    session_local = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    return engine, session_local

def get_db_factory(db_key: str):
    """
    Returns a dependency function for FastAPI to inject a DB session
    tied to the given db_key.
    """
    _, session_local = create_engine_and_session(db_key)
    
    async def get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_local() as session:
            try:
                yield session
            except Exception as e:
                logger.error(f"Database session error: {str(e)}")
                await session.rollback()
                raise
            finally:
                await session.close()
    
    return get_db