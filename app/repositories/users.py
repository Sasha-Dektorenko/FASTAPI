from sqlalchemy import select
from ..models.user import User
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import UserOut
from datetime import datetime
from ..core.exceptions import BaseAppException, NotFoundException
import logging


logger = logging.getLogger(__name__)

class UserRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    
    async def select_all_users(self, offset: int, limit: int) -> Sequence[User]:
        stmt = select(User).offset(offset).limit(limit)
        users = await self.db_session.scalars(stmt)
        return users.all()
       
    
    async def create_user(self, user: User) -> User:
        self.db_session.add(user)
        await self.db_session.flush()
        return user
    
    
    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        user = await self.db_session.scalars(stmt)
        return user.first() if user else None
        
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        user = await self.db_session.get(User, user_id)
        return user 
        
    
    async def update_user(self, user: User, new_data: dict) -> User | None:
        for key, value in new_data.items():
            setattr(user, key, value)
        await self.db_session.flush()
        return user if user else None
