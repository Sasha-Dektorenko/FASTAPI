from datetime import datetime
from pydantic import BaseModel

class UserModel(BaseModel):
    fullname: str
    username: str
    password: str

class UserOut(BaseModel):
    id: str
    fullname: str
    username: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class Users(BaseModel):
    total: int
    offset: int
    limit: int
    data : list[UserOut]
    model_config = {"from_attributes": True}

class UserPatch(BaseModel):
    fullname: str | None = None
    username: str | None = None
    password: str | None = None
    
    
