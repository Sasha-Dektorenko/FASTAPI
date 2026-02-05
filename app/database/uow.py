from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.users import UserRepository
from ..repositories.posts import PostsRepository    
from fastapi import Depends
from .db import get_session

class Uow:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.user_repo = UserRepository(db_session)
        self.post_repo = PostsRepository(db_session)

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            await self.db_session.rollback()
        else:
            await self.db_session.commit()

        await self.db_session.close()

def get_uow(session: AsyncSession = Depends(get_session)) -> Uow:
    return Uow(session)