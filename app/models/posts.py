from ..database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING: 
    from .user import User

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key = True)
    title: Mapped[str] = mapped_column(String(30), unique=True)
    content: Mapped[str]

    user_id:Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))  

    author: Mapped["User"] = relationship(back_populates="posts") 
