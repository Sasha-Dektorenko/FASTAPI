from sqlalchemy import select
from ..models import Post, User
from ..schemas import PostOut
from typing import Sequence
from sqlalchemy.orm import Session
import logging 
from ..core.exceptions import BaseAppException, NotFoundException

logger = logging.getLogger(__name__)


class PostsRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session


    def get_post_by_id(self, post_id: int) -> PostOut:
        post = self.db_session.get(Post, post_id)
        if not post:
            raise NotFoundException(f"Post with ID: {post_id} not found")
        return PostOut.model_validate(post) 
        

    def get_post_by_title(self, title: str) -> Post | None:
        stmt = select(Post).where(Post.title == title)
        post = self.db_session.scalars(stmt).first()
        return post if post else None
        

    def select_all_posts(self, offset: int, limit: int) -> Sequence[Post]:
        stmt = select(Post).offset(offset).limit(limit)
        posts = self.db_session.scalars(stmt).all()
        return posts
        
    
    def create_post(self, post: Post) -> PostOut:
        self.db_session.add(post)
        self.db_session.flush()
        return PostOut.model_validate(post)
    
    
    def update_post(self, post: Post, new_data: dict) -> PostOut:
        for key, value in new_data.items():
            setattr(post, key, value)
        self.db_session.flush()
        return PostOut.model_validate(post)
    
    
    def update_post_users(self, post: Post, user: User) -> PostOut:
        if user not in post.users:
            post.users.append(user)
        self.db_session.flush()
        return PostOut.model_validate(post)