from sqlalchemy import select
from ..models import User
from ..database import SessionDep
from typing import Sequence
from sqlalchemy.orm import Session


class UserRepository:
    @staticmethod
    def select_all_users(db: Session, offset: int, limit: int) -> Sequence[User]:
        stmt = select(User).offset(offset).limit(limit)
        print(stmt)
        users = db.scalars(stmt).all()
        return users

