from sqlalchemy import select
from ..models import Post, User
from ..schemas import PostOut
from typing import Sequence
from sqlalchemy.orm import Session
import logging 
from ..core.exceptions import BaseAppException, NotFoundException

logger = logging.getLogger(__name__)


class PostsRepository:
    @staticmethod
    def get_post_by_id(db: Session, post_id: int) -> PostOut:
        try:
            post = db.get(Post, post_id)
            if not post:
                raise NotFoundException(f"Post with ID: {post_id} not found")
            return PostOut.model_validate(post) 
        except Exception as e:
            raise BaseAppException("Database error occured while fetching post by ID") from e
        
        
    
    @staticmethod
    def get_post_by_title(db: Session, title: str) -> Post:
        try: 
            
            stmt = select(Post).where(Post.title == title)
            post = db.scalars(stmt).first()
            if not post:
                raise NotFoundException(f"Post with title: {title} not found")
            return post
        except Exception as e:
            raise BaseAppException("Database error occured while fetching post by title") from e
        
    
    @staticmethod
    def select_all_posts(db: Session, offset: int, limit: int) -> Sequence[Post]:
        try:
            stmt = select(Post).offset(offset).limit(limit)
            posts = db.scalars(stmt).all()
            if not posts:
                raise NotFoundException("No posts found")
            return posts
        except Exception as e:
            raise BaseAppException("Database error occured while fetching all posts") from e
        
        
    
    @staticmethod
    def create_post(db: Session, post: Post) -> PostOut:
        db.add(post)
        db.commit()
        db.refresh(post)
        return PostOut.model_validate(post)
    
    @staticmethod
    def update_post(db: Session, post: Post, new_data: dict) -> PostOut:
        for key, value in new_data.items():
            setattr(post, key, value)
        db.commit()
        db.refresh(post)
        return PostOut.model_validate(post)
    
    @staticmethod
    def update_post_users(db: Session, post: Post, user: User) -> PostOut:
        post.users.append(user)
        db.commit()
        db.refresh(post)
        return PostOut.model_validate(post)