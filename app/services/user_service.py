from ..schemas import UserOut, Users
from ..repositories import UserRepository
from ..database import SessionDep
from sqlalchemy.orm import Session


class UserService:
    @staticmethod
    def get_users(db: Session, offset: int, limit: int) -> Users:
        users = UserRepository.select_all_users(db, offset, limit)
        print(users)
        total = len(users)
        users = [UserOut.model_validate(user) for user in users]
        return Users(
            total = total,
            offset = offset,
            limit = limit,
            data = users 
        )