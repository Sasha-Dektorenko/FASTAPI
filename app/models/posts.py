from ..database.db import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.association_table import association_table
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING: 
    from .user import User

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String(30), unique=True)
    content: Mapped[str]

    users: Mapped[list["User"]] = relationship(secondary=association_table, back_populates="posts") 
