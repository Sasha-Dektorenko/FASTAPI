from sqlalchemy import select
from ..models import User
from typing import Sequence
from sqlalchemy.orm import Session
from ..schemas import UserOut, UserModel
from datetime import datetime



class UserRepository:
    @staticmethod
    def select_all_users(db: Session, offset: int, limit: int) -> Sequence[User]:
        stmt = select(User).offset(offset).limit(limit)
        print(stmt)
        users = db.scalars(stmt).all()
        return users
    
    @staticmethod
    def create_user(db: Session, user: User) -> UserOut:
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserOut.model_validate(user)
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        user = db.scalars(stmt).first()
        return user if user else None
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        user = db.get(User, user_id)
        return user if user else None
    
    @staticmethod
    def update_user(db: Session, user: User, new_data: dict) -> UserOut:
        for key, value in new_data.items():
            setattr(user, key, value)
        user.updated_at = datetime.now()
        db.commit()
        db.refresh(user)
        return UserOut.model_validate(user)
