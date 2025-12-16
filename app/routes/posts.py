from fastapi import APIRouter
from ..schemas import PostModel, PostOut, PostPatch, Posts
from ..database import SessionDep
from ..services import PostService
import logging

logger = logging.getLogger(__name__)

post_router = APIRouter(prefix = "/api/v1/posts")


@post_router.get("/{post_id}", response_model= PostOut)
async def get_post(post_id: int, db: SessionDep):
    return PostService.get_post_by_id(db, post_id)
    

