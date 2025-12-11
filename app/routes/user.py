from fastapi import APIRouter, HTTPException, Depends
from ..schemas import UserOut, UserModel, Users, UserPatch, PostOut, PostModel, Posts
from ..database import SessionDep
from ..models import User, Post
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..services import UserService

user_router = APIRouter(prefix = "/api/v1/users")

@user_router.get("/{user_id}", response_model= UserOut)
async def get_user(user_id: int, db: SessionDep):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User with id {user_id} doesn't exist")
    return user
    

@user_router.get("/", response_model=Users)
def get_users( db: SessionDep, offset:int = 0, limit: int = 5,):
    return UserService.get_users(db, offset, limit)

@user_router.post("/reg", response_model=UserOut,status_code=201)
async def create_user(user_data: UserModel, db: SessionDep):
    exists = db.query(User).filter(User.username == user_data.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="User with this username already exists")
    
    user = User(fullname=user_data.fullname,
                 username = user_data.username, 
                 password = user_data.password)
    
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
    

@user_router.patch("/update/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_update: UserPatch, db: SessionDep):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    
    new_data = user_update.model_dump(exclude_unset=True)
    for key, value in new_data.items():
        setattr(user, key, value)
        
    user.updated_at = datetime.now()

    db.commit()
    db.refresh(user)

    return user

@user_router.post("/{user_id}/post", response_model=PostOut)
async def make_post(user_id: int, post_data: PostModel, db: SessionDep):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    post = Post(title = post_data.title, 
                content = post_data.content,
                user_id = user.id
                )

    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@user_router.get("/{user_id}/posts", response_model=Posts)
async def user_posts(user_id: int, db: SessionDep, offset:int = 0, limit: int = 5, ):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    
    posts = user.posts [offset:offset+limit]
    total = len(user.posts)

    return Posts(
        total = total,
        offset = offset,
        limit = limit,
        author = user, # type: ignore
        posts = posts
    )

    




