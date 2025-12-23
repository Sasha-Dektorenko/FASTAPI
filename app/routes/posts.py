from fastapi import APIRouter, Depends
from ..schemas import PostModel, PostOut, PostPatch, Posts
from ..database import SessionDep
from ..services import get_post_service, PostService
import logging

logger = logging.getLogger(__name__)

post_router = APIRouter(prefix = "/api/v1/posts")


@post_router.get("/{post_id}", response_model= PostOut)
async def get_post(post_id: int, post_service: PostService = Depends(get_post_service)):
    return post_service.get_post_by_id(post_id)
    

