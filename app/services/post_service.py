from sqlalchemy.orm import Session
from ..schemas import PostOut, PostModel, Posts, UserOut
from ..repositories import PostsRepository, UserRepository
from ..models import Post
from ..core.exceptions import BaseAppException, NotFoundException, ValidationException
from ..database.uow import get_uow
from fastapi import Depends
from ..database.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
import logging


logger = logging.getLogger(__name__)

def get_post_service(db: AsyncSession = Depends(get_session)) -> "PostService":
    return PostService(db)


class PostService:
    def __init__(self, db: AsyncSession):
        self.db = db

    
    async def get_post_by_id(self, post_id: int) -> PostOut:
        async with get_uow(self.db) as uow:
            logger.info(f"Fetching post by ID: {post_id}")
            post = await uow.post_repo.get_post_by_id(post_id)
            if not post:
                raise NotFoundException(f"Post with ID: {post_id} not found")
            return PostOut.model_validate(post)
        
    async def get_posts(self, user_id: int, offset: int, limit: int) -> Posts:
        async with get_uow(self.db) as uow:
            logger.info("Fetching user by ID before fetching posts")
            user = await uow.user_repo.get_user_by_id(user_id)
        
            logger.info("Fetching posts from database")
            posts = await uow.post_repo.select_all_posts(offset, limit)
            total = len(posts)
            posts = [PostOut.model_validate(post) for post in posts]

            return Posts(
                total = total, 
                offset = offset,
                limit = limit,
                posts = posts,    
            )
        
        
    
    async def create_post(self, user_id: int, post_data: PostModel) -> PostOut:
        async with get_uow(self.db) as uow:
            logger.info("Fetching user by ID before creating post")
            user = await uow.user_repo.get_user_by_id(user_id)
            if not user:
                raise NotFoundException(f"User with ID: {user_id} not found")

            logger.info("Checking if post with the same title exists")
            post = await uow.post_repo.get_post_by_title(post_data.title)

            if post:
                postout = await uow.post_repo.update_post_users(post, user)
                return PostOut.model_validate(postout)
                 

            post = Post(
                title=post_data.title,
                content=post_data.content,
                users = [user]
                )
        
            return PostOut.model_validate(uow.post_repo.create_post(post))
        

            
        
        

        