from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated
from fastapi import Depends
from ..core.config import DB_URL


engine = create_async_engine(DB_URL, echo=True)

sessionlocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

async def get_session():
    db_session = sessionlocal()
    try:
        yield db_session
    except Exception:
        await db_session.rollback()
        raise
    finally:
        await db_session.close()




