from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from typing import Annotated
from fastapi import Depends
from ..core.config import DB_URL


engine = create_engine(DB_URL, echo = True, connect_args={"check_same_thread": False})

class Base(DeclarativeBase):
    pass

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


