from sqlalchemy import select
from ..models import Post, User
from ..schemas import PostOut
from typing import Sequence
from sqlalchemy.orm import Session



class PostsRepository:
    @staticmethod
    def get_post_by_id(db: Session, post_id: int) -> PostOut | None:
        post = db.get(Post, post_id)
        return PostOut.model_validate(post) if post else None
    
    @staticmethod
    def get_post_by_title(db: Session, title: str) -> Post | None:
        stmt = select(Post).where(Post.title == title)
        post = db.scalars(stmt).first()
        return post if post else None
    
    @staticmethod
    def select_all_posts(db: Session, offset: int, limit: int) -> Sequence[Post]:
        stmt = select(Post).offset(offset).limit(limit)
        posts = db.scalars(stmt).all()
        return posts
    
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