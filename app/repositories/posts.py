from sqlalchemy import select
from ..models import Post
from ..schemas import PostOut, PostModel
from typing import Sequence
from sqlalchemy.orm import Session



class PostsRepository:
    @staticmethod
    def get_post_by_id(db: Session, post_id: int) -> PostOut | None:
        post = db.get(Post, post_id)
        return PostOut.model_validate(post) if post else None
    
    @staticmethod
    def select_all_posts(db: Session, offset: int, limit: int) -> Sequence[Post]:
        stmt = select(Post).offset(offset).limit(limit)
        posts = db.scalars(stmt).all()
        return posts
    
    @staticmethod
    def create_post(db: Session, post: PostModel) -> PostOut:
        db.add(post)
        db.commit()
        db.refresh(post)
        return PostOut.model_validate(post)