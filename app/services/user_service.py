from ..schemas import UserOut, Users, UserModel, UserPatch, LoginModel, TokenOut
from ..models.user import User
from ..core import BaseAppException, NotFoundException, ConflictException, ValidationException, hash_password
from ..database.uow import get_uow
from sqlalchemy.orm import Session
from .auth_service import AuthService
from ..core import verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from ..database.db import get_session


import logging

logger = logging.getLogger(__name__)

def get_user_service(db: AsyncSession = Depends(get_session)) -> "UserService":
    return UserService(db)

class UserService:

    def __init__(self, db: AsyncSession):
        self.db = db
    

    async def get_user_by_id(self, user_id: int) -> UserOut | None:
        async with get_uow(self.db) as uow:
            logger.info(f"Fetching user by ID: {user_id}")
            user = await uow.user_repo.get_user_by_id(user_id)
            if not user:
                raise NotFoundException("User not found")
            return UserOut.model_validate(user)
        

    async def get_users(self, offset: int, limit: int) -> Users:
        async with get_uow(self.db) as uow:
            logger.info("Fetching users from database")
            users = await uow.user_repo.select_all_users (offset, limit)
            total = len(users)
            users = [UserOut.model_validate(user) for user in users]
            return Users(
                total = total,
                offset = offset,
                limit = limit,
                data = users 
            )
       
    
    async def create_user(self, user_data: UserModel) -> UserOut:
        async with get_uow(self.db) as uow:
            logger.info("Checking if user with the same username exists")
            exists = await uow.user_repo.get_user_by_username (user_data.username)
            if exists:
                raise ConflictException("User with the same username already exists")
            
            user = User(
                    fullname=user_data.fullname,
                    username = user_data.username, 
                    password = hash_password(user_data.password),
                    )
            userout = await uow.user_repo.create_user(user)
            token_payload = {
                "sub": userout.id,
            }
            token = AuthService.create_access_token(token_payload)

            print(f"User created with token: {token}")  
            return UserOut.model_validate(userout)
            
    
    
    async def update_user(self, user_id: int, user_data: UserPatch) -> UserOut:
        async with get_uow(self.db) as uow:
            logger.info(f"Fetching user by ID: {user_id}")
            user = await uow.user_repo.get_user_by_id(user_id)
            if not user:
                raise NotFoundException("User not found")
        
            try:
                new_data = user_data.model_dump(exclude_unset=True)
                userout = await uow.user_repo.update_user(user, new_data)
                return UserOut.model_validate(userout)
            except Exception as e:
                raise BaseAppException("Unexpected internal error occured while updating user") from e
            
            
    async def login_user(self, username: str, password: str) -> TokenOut:
        async with get_uow(self.db) as uow:
            logger.info(f"Fetching user by username: {username}")
            user = await uow.user_repo.get_user_by_username(username)
            if not user or not verify_password(password, user.password):
                raise ValidationException("Invalid username or password")
            
            token_payload = {
                "sub": user.id,
            }
            token = AuthService.create_access_token(token_payload)
            return TokenOut(access_token=token)
        
    async def login_google_user(self, user_info: dict) -> TokenOut:
        async with get_uow(self.db) as uow:
            logger.info(f"Checking if user with Google ID: {user_info['sub']} exists")
            user = await uow.user_repo.get_user_by_id(user_info["sub"])
            if not user:
                logger.info("User not found, creating new user")
                user = User(
                    id = user_info["sub"],
                    fullname=user_info.get("name", ""),
                    username = user_info.get("email", ""),
                    )
                user = await uow.user_repo.create_user(user)
            
            token_payload = {
                "sub": user.id,
            }
            token = AuthService.create_access_token(token_payload)
            return TokenOut(access_token=token)
        
        