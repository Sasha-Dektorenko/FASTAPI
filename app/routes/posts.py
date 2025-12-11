from fastapi import APIRouter, HTTPException, Depends
from ..schemas import PostModel, PostOut, PostPatch, Posts
from ..database import SessionDep
from ..models import Post
from sqlalchemy.orm import Session

post_router = APIRouter(prefix = "/api/v1/posts")

@post_router.get("/{post_id}", response_model= PostOut)
async def get_post(post_id: int, db: SessionDep):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail ="Post doesn't exist")
    return post

