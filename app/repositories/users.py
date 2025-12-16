from sqlalchemy import select
from ..models import User
from typing import Sequence
from sqlalchemy.orm import Session
from ..schemas import UserOut
from datetime import datetime
from ..core.exceptions import BaseAppException, NotFoundException
import logging


logger = logging.getLogger(__name__)



class UserRepository:
    @staticmethod
    def select_all_users(db: Session, offset: int, limit: int) -> Sequence[User]:
        try:
            stmt = select(User).offset(offset).limit(limit)
            users = db.scalars(stmt).all()
            if not users:
                raise NotFoundException("No users found")
            return users
        except Exception as e:
            raise BaseAppException("Database error occured while fetching all users") from e
        
    @staticmethod
    def create_user(db: Session, user: User) -> UserOut:
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserOut.model_validate(user)
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        try: 
            stmt = select(User).where(User.username == username)
            user = db.scalars(stmt).first()
            return user if user else None
        except Exception as e:
            raise BaseAppException("Database error occured while fetching user by username") from e
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        try:
            user = db.get(User, user_id)
            if not user:
                raise NotFoundException("User not found")
            return user 
        except Exception as e:
            raise BaseAppException("Database error occured while fetching user by ID") from e
        
    @staticmethod
    def update_user(db: Session, user: User, new_data: dict) -> UserOut:
        for key, value in new_data.items():
            setattr(user, key, value)
        user.updated_at = datetime.now()
        db.commit()
        db.refresh(user)
        return UserOut.model_validate(user)
