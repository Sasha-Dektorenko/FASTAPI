from ..schemas import UserOut, Users, UserModel, UserPatch
from ..models import User
from ..core import BaseAppException, NotFoundException, ConflictException, ValidationException, hash_password
from ..database import get_uow, SessionDep
from sqlalchemy.orm import Session
from .auth_service import AuthService
import logging

logger = logging.getLogger(__name__)

def get_user_service(db: SessionDep) -> "UserService":
    return UserService(db)

class UserService:

    def __init__(self, db: Session):
        self.db = db
    

    def get_user_by_id(self, user_id: int) -> UserOut | None:
        with get_uow(self.db) as uow:
            logger.info(f"Fetching user by ID: {user_id}")
            user = uow.user_repo.get_user_by_id(user_id)
            if not user:
                raise NotFoundException("User not found")
            return UserOut.model_validate(user)
        

    def get_users(self, offset: int, limit: int) -> Users:
        with get_uow(self.db) as uow:
            logger.info("Fetching users from database")
            users = uow.user_repo.select_all_users (offset, limit)
            total = len(users)
            users = [UserOut.model_validate(user) for user in users]
            return Users(
                total = total,
                offset = offset,
                limit = limit,
                data = users 
            )
       
    
    def create_user(self, user_data: UserModel) -> UserOut:
        with get_uow(self.db) as uow:
            logger.info("Checking if user with the same username exists")
            exists = uow.user_repo.get_user_by_username (user_data.username)
            if exists:
                raise ConflictException("User with the same username already exists")
            
            user = User(
                    fullname=user_data.fullname,
                    username = user_data.username, 
                    password = hash_password(user_data.password),
                    )
            userout = uow.user_repo.create_user(user)
            token_payload = {
                "sub": userout.id,
            }
            token = AuthService.create_access_token(token_payload)

            print(f"User created with token: {token}")  
            return UserOut.model_validate(userout)
            
    
    
    def update_user(self, user_id: int, user_data: UserPatch) -> UserOut:
        with get_uow(self.db) as uow:
            logger.info(f"Fetching user by ID: {user_id}")
            user = uow.user_repo.get_user_by_id(user_id)
            if not user:
                raise NotFoundException("User not found")
        
            try:
                new_data = user_data.model_dump(exclude_unset=True)
                userout = uow.user_repo.update_user(user, new_data)
                return UserOut.model_validate(userout)
            except Exception as e:
                raise BaseAppException("Unexpected internal error occured while updating user") from e
        