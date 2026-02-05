from pydantic import BaseModel
from ..schemas import UserOut

class PostModel(BaseModel):
    title: str 
    content: str | None = None
    
class PostOut(BaseModel):
    id: str
    title: str
    content: str
    users: list[UserOut]
    model_config = {"from_attributes": True}


class Posts(BaseModel):
    total: int
    offset: int
    limit: int
    posts : list[PostOut]
    
    model_config = {"from_attributes": True}

class PostPatch(BaseModel):
    title: str | None = None
    content: str | None = None