from ..schemas import UserOut, Users, UserModel, UserPatch
from ..repositories import UserRepository
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import User
from ..core.exceptions import BaseAppException, NotFoundException, ConflictException
import logging

logger = logging.getLogger(__name__)



class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> UserOut | None:
        try:
            logger.info(f"Fetching user by ID: {user_id}")
            user = UserRepository.get_user_by_id(db, user_id)
            return UserOut.model_validate(user)
        except NotFoundException:
            raise
        except Exception as e:
            raise BaseAppException(f"Unexpected database error occured while fetching user by ID: {user_id}") from e

    @staticmethod
    def get_users(db: Session, offset: int, limit: int) -> Users:
        try:
            logger.info("Fetching users from database")
            users = UserRepository.select_all_users(db, offset, limit)
            total = len(users)
            users = [UserOut.model_validate(user) for user in users]
            return Users(
                total = total,
                offset = offset,
                limit = limit,
                data = users 
            )
        except NotFoundException:
            raise
        except Exception as e:
            raise BaseAppException("Unexpected database error occured while fetching users") from e
    
    @staticmethod
    def create_user(db: Session, user_data: UserModel) -> UserOut:
        try:
            logger.info("Checking if user with the same username exists")
            exists = UserRepository.get_user_by_username(db, user_data.username)
            if exists:
                raise ConflictException("User with the same username already exists")
        except Exception as e:
            raise BaseAppException("Unexpected database error occured while checking for existing username") from e
    
        user = User(
                fullname=user_data.fullname,
                username = user_data.username, 
                password = user_data.password,
                )
        
        return UserRepository.create_user(db, user)
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserPatch) -> UserOut:
        try:
            logger.info(f"Fetching user by ID: {user_id}")
            user = UserRepository.get_user_by_id(db, user_id)
        except NotFoundException:
            raise
        except Exception as e:
            raise BaseAppException(f"Unexpected database error occured while fetching user by ID: {user_id}") from e
        
        new_data = user_data.model_dump(exclude_unset=True)
        
        return UserRepository.update_user(db, user, new_data)