from database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key = True)
    title: Mapped[str] = mapped_column(String(30), unique=True)
    content: Mapped[str]

    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))  

    author: Mapped["User"] = relationship(back_populates="posts") # type: ignore

