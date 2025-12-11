from pydantic import BaseModel
from ..schemas import UserOut

class PostModel(BaseModel):
    title: str | None = None
    content: str
    
class PostOut(BaseModel):
    id: int
    title: str
    content: str
    author: UserOut
    model_config = {"from_attributes": True}

class PostForList(BaseModel):
    id: int
    title: str
    content: str
    model_config = {"from_attributes": True}

class Posts(BaseModel):
    total: int
    offset: int
    limit: int
    author: UserOut
    posts : list[PostForList]
    
    model_config = {"from_attributes": True}

class PostPatch(BaseModel):
    title: str | None = None
    content: str | None = None