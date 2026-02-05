from datetime import datetime, timezone
from ..database.db import Base
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.association_table import association_table
from typing import TYPE_CHECKING
from uuid import uuid4


if TYPE_CHECKING: 
    from .posts import Post

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    fullname: Mapped[str] = mapped_column(String(40))
    username: Mapped[str] = mapped_column(String(254), unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                                                 onupdate=lambda: datetime.now(timezone.utc))

    posts: Mapped[list["Post"]] = relationship(secondary=association_table,back_populates="users") 

    