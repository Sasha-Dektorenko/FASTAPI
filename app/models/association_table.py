from ..database import Base
from sqlalchemy import Table, Column, ForeignKey

association_table = Table(
    'association',
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
)