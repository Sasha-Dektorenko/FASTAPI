from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_URL = "sqlite:///./database.db"

engine = create_engine(DB_URL, echo = True, connect_args={"check_same_thread": False})

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit = False)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
    
