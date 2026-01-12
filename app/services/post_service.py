from sqlalchemy.orm import Session
from ..schemas import PostOut, PostModel, Posts, UserOut
from ..repositories import PostsRepository, UserRepository
from ..models import Post
from ..core.exceptions import BaseAppException, NotFoundException, ValidationException
from ..database import get_uow, SessionDep
import logging


logger = logging.getLogger(__name__)

def get_post_service(db: SessionDep) -> "PostService":
    return PostService(db)


class PostService:
    def __init__(self, db: Session):
        self.db = db

    
    def get_post_by_id(self, post_id: int) -> PostOut:
        with get_uow(self.db) as uow:
            logger.info(f"Fetching post by ID: {post_id}")
            post = uow.post_repo.get_post_by_id(post_id)
            if not post:
                raise NotFoundException(f"Post with ID: {post_id} not found")
            return PostOut.model_validate(post)
        
    def get_posts(self, user_id: int, offset: int, limit: int) -> Posts:
        with get_uow(self.db) as uow:
            logger.info("Fetching user by ID before fetching posts")
            user = uow.user_repo.get_user_by_id(user_id)
        
            logger.info("Fetching posts from database")
            posts = uow.post_repo.select_all_posts(offset, limit)
            total = len(posts)
            posts = [PostOut.model_validate(post) for post in posts]

            return Posts(
                total = total, 
                offset = offset,
                limit = limit,
                posts = posts,    
            )
        
        
    
    def create_post(self, user_id: int, post_data: PostModel) -> PostOut:
        with get_uow(self.db) as uow:
            logger.info("Fetching user by ID before creating post")
            user = uow.user_repo.get_user_by_id(user_id)
            if not user:
                raise NotFoundException(f"User with ID: {user_id} not found")

            logger.info("Checking if post with the same title exists")
            post = uow.post_repo.get_post_by_title(post_data.title)

            if post:
                postout = uow.post_repo.update_post_users(post, user)
                return PostOut.model_validate(postout)
                 

            post = Post(
                title=post_data.title,
                content=post_data.content,
                users = [user]
                )
        
            return PostOut.model_validate(uow.post_repo.create_post(post))
        

            
        
        

        