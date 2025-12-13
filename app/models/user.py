from datetime import datetime
from ..database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.association_table import association_table
from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from .posts import Post

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(40))
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    posts: Mapped[list["Post"]] = relationship(secondary=association_table,back_populates="users") 

    @property
    def mask_password(self):
        return "*" * len(self.password)
    
    @mask_password.setter
    def set_password(self, new_pass):
        self.password = new_pass