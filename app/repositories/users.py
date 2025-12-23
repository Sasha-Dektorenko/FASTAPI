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

    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    
    def select_all_users(self, offset: int, limit: int) -> Sequence[User]:
        stmt = select(User).offset(offset).limit(limit)
        users = self.db_session.scalars(stmt).all()
        return users
       
    
    def create_user(self, user: User) -> UserOut:
        self.db_session.add(user)
        self.db_session.flush()
        return UserOut.model_validate(user)
    
    
    def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        user = self.db_session.scalars(stmt).first()
        return user if user else None
        
    
    
    def get_user_by_id(self, user_id: int) -> User:
        user = self.db_session.get(User, user_id)
        if not user:
            raise NotFoundException("User not found")
        return user 
        
    
    def update_user(self, user: User, new_data: dict) -> UserOut:
        for key, value in new_data.items():
            setattr(user, key, value)
        self.db_session.flush()
        return UserOut.model_validate(user)
