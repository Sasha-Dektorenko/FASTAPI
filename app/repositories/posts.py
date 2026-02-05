from sqlalchemy import select
from ..models import Post, User
from ..schemas import PostOut
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
import logging 
from ..core.exceptions import BaseAppException, NotFoundException

logger = logging.getLogger(__name__)


class PostsRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


    async def get_post_by_id(self, post_id: int) -> Post | None:
        post = await self.db_session.get(Post, post_id)
        return post if post else None
        

    async def get_post_by_title(self, title: str) -> Post | None:
        stmt = select(Post).where(Post.title == title)
        post = await self.db_session.scalars(stmt)
        return post.first() if post else None
        

    async def select_all_posts(self, offset: int, limit: int) -> Sequence[Post]:
        stmt = select(Post).offset(offset).limit(limit)
        posts = await self.db_session.scalars(stmt)
        return posts.all()
        
    
    async def create_post(self, post: Post) -> Post:
        self.db_session.add(post)
        await self.db_session.flush()
        return post
    
    
    async def update_post(self, post: Post, new_data: dict) -> Post | None:
        for key, value in new_data.items():
            setattr(post, key, value)
        await self.db_session.flush()
        return post if post else None
    
    
    async def update_post_users(self, post: Post, user: User) -> Post | None:
        if user not in post.users:
            post.users.append(user)
        await self.db_session.flush()
        return post if post else None