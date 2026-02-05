from fastapi import APIRouter, Depends
from ..schemas import UserOut, UserModel, Users, UserPatch, PostOut, PostModel, Posts
from ..services import UserService, PostService, get_user_service, get_post_service
from ..core.dependencies import get_current_user

user_router = APIRouter(prefix = "/api/v1/users")


@user_router.get("/", response_model=Users)
async def get_users(user_service: UserService = Depends(get_user_service), offset:int = 0, limit: int = 5,):
    return await user_service.get_users(offset, limit)
    
@user_router.patch("/update", response_model=UserOut)
async def update_user(user_data: UserPatch, current_user = Depends(get_current_user), user_service: UserService = Depends(get_user_service)):
    return await user_service.update_user(current_user.id, user_data)
        
@user_router.post("/make_post", response_model=PostOut)
async def make_post(post_data: PostModel, current_user = Depends(get_current_user), post_service: PostService = Depends(get_post_service)):
    return await post_service.create_post(current_user.id, post_data)
    
@user_router.get("/my_posts", response_model=Posts)
async def user_posts(post_service: PostService = Depends(get_post_service), current_user = Depends(get_current_user), offset:int = 0, limit: int = 5, ):
    return await post_service.get_posts(current_user.id, offset, limit)
    
@user_router.get("/me", response_model=UserOut)
async def me(current_user: UserOut = Depends(get_current_user)):
    return current_user
    




