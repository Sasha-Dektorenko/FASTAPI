from fastapi import APIRouter, Depends
from ..schemas import UserOut, UserModel, Users, UserPatch, PostOut, PostModel, Posts
from ..database import SessionDep
from ..services import UserService, PostService, get_user_service, get_post_service

user_router = APIRouter(prefix = "/api/v1/users")


@user_router.get("/{user_id}", response_model= UserOut)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    return user_service.get_user_by_id(user_id)
        
@user_router.get("/", response_model=Users)
def get_users(user_service: UserService = Depends(get_user_service), offset:int = 0, limit: int = 5,):
    return user_service.get_users(offset, limit)
    
@user_router.patch("/update/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_data: UserPatch, user_service: UserService = Depends(get_user_service)):
    return user_service.update_user(user_id, user_data)
        
@user_router.post("/{user_id}/post", response_model=PostOut)
async def make_post(user_id: int, post_data: PostModel, post_service: PostService = Depends(get_post_service)):
    return post_service.create_post(user_id, post_data)
    
@user_router.get("/{user_id}/posts", response_model=Posts)
async def user_posts(user_id: int, post_service: PostService = Depends(get_post_service), offset:int = 0, limit: int = 5, ):
    return post_service.get_posts(user_id, offset, limit)
    

    




