from sqlalchemy.orm import Session
from ..repositories.users import UserRepository
from ..repositories.posts import PostsRepository    
from .db import SessionDep

class Uow:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.user_repo = UserRepository(db_session)
        self.post_repo = PostsRepository(db_session)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.db_session.rollback()
        else:
            self.db_session.commit()

        self.db_session.close()

def get_uow(session: SessionDep) -> Uow:
    return Uow(session)