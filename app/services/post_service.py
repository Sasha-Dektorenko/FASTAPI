from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..schemas import PostOut, PostModel, Posts, UserOut
from ..repositories import PostsRepository, UserRepository
from ..models import Post


class PostService:
    @staticmethod
    def get_post_by_id(db: Session, post_id: int) -> PostOut:
        post = PostsRepository.get_post_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post doesn't exist")
        return post
    
    
    @staticmethod
    def get_posts(db: Session, user_id: int, offset: int, limit: int) -> Posts:
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User doesn't exist")
        
        
        posts = PostsRepository.select_all_posts(db, offset, limit)
        total = len(posts)
        posts = [PostOut.model_validate(post) for post in posts]

        return Posts(
            total = total, 
            offset = offset,
            limit = limit,
            posts = posts,    
        )
        
    @staticmethod
    def create_post(db: Session, user_id: int, post_data: PostModel) -> PostOut:
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User doesn't exist")
        
        post = PostsRepository.get_post_by_title(db, post_data.title)

        if post:
            PostsRepository.update_post_users(db, post, user)
            return PostOut.model_validate(post)

        post = Post(
            title=post_data.title,
            content=post_data.content,
            users = [user]
            )
        
        return PostsRepository.create_post(db, post)

            
        
        

        