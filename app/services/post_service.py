from sqlalchemy.orm import Session
from ..schemas import PostOut, PostModel, Posts, UserOut
from ..repositories import PostsRepository, UserRepository
from ..models import Post
from ..core.exceptions import BaseAppException, NotFoundException
import logging


logger = logging.getLogger(__name__)


class PostService:
    @staticmethod
    def get_post_by_id(db: Session, post_id: int) -> PostOut:
        try:
            logger.info(f"Fetching post by ID: {post_id}")
            post = PostsRepository.get_post_by_id(db, post_id)
            return post
        except BaseAppException as e:
            raise 
        except Exception as e:
            raise BaseAppException(f"Unexpected database error occured while fetching post by ID: {post_id}") from e
    
    
    @staticmethod
    def get_posts(db: Session, user_id: int, offset: int, limit: int) -> Posts:
        try:
            logger.info("Fetching user by ID before fetching posts")
            user = UserRepository.get_user_by_id(db, user_id)
        except NotFoundException:
            raise 
        except Exception as e:
            raise BaseAppException(f"Unexpected database error occured while fetching user by ID: {user_id}") from e
        
        try:
            logger.info("Fetching posts from database")
            posts = PostsRepository.select_all_posts(db, offset, limit)
            total = len(posts)
            posts = [PostOut.model_validate(post) for post in posts]

            return Posts(
                total = total, 
                offset = offset,
                limit = limit,
                posts = posts,    
            )
        except NotFoundException:
            raise
        except Exception as e:
            raise BaseAppException("Unexpected database error occured while fetching posts") from e
        
    @staticmethod
    def create_post(db: Session, user_id: int, post_data: PostModel) -> PostOut:
        try:
            logger.info("Fetching user by ID before creating post")
            user = UserRepository.get_user_by_id(db, user_id)
        except NotFoundException:
            raise 
        except Exception as e:
            raise BaseAppException(f"Unexpected database error occured while fetching user by ID: {user_id}") from e
        
        
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

            
        
        

        