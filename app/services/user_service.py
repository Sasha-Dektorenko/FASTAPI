from ..schemas import UserOut, Users, UserModel, UserPatch
from ..repositories import UserRepository
from sqlalchemy.orm import Session
from fastapi import HTTPException



class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> UserOut | None:
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User doesn't exist")
        return UserOut.model_validate(user)

    @staticmethod
    def get_users(db: Session, offset: int, limit: int) -> Users:
        users = UserRepository.select_all_users(db, offset, limit)
        total = len(users)
        users = [UserOut.model_validate(user) for user in users]
        return Users(
            total = total,
            offset = offset,
            limit = limit,
            data = users 
        )
    
    @staticmethod
    def create_user(db: Session, user: UserModel) -> UserOut:
        exists = UserRepository.get_user_by_username(db, user.username)
        if exists:
            raise HTTPException(status_code=400, detail="User with this username already exists")
    
        user = UserModel(fullname=user.fullname,
                 username = user.username, 
                 password = user.password)
        return UserRepository.create_user(db, user)
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserPatch) -> UserOut:
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User doesn't exist")
        
        new_data = user_data.model_dump(exclude_unset=True)
        
        return UserRepository.update_user(db, user, new_data)