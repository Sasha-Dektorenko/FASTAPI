from fastapi import APIRouter
from ..schemas import UserOut, UserModel, Users, UserPatch, PostOut, PostModel, Posts
from ..database import SessionDep
from ..services import UserService, PostService


user_router = APIRouter(prefix = "/api/v1/users")

@user_router.get("/{user_id}", response_model= UserOut)
async def get_user(user_id: int, db: SessionDep):
    return UserService.get_user_by_id(db, user_id)
        
    
    

@user_router.get("/", response_model=Users)
def get_users( db: SessionDep, offset:int = 0, limit: int = 5,):
    return UserService.get_users(db, offset, limit)


@user_router.post("/reg", response_model=UserOut,status_code=201)
async def create_user(user_data: UserModel, db: SessionDep):
    return UserService.create_user(db, user_data)
        
    
    
    
@user_router.patch("/update/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_data: UserPatch, db: SessionDep):
    return UserService.update_user(db, user_id, user_data)
        
   

@user_router.post("/{user_id}/post", response_model=PostOut)
async def make_post(user_id: int, post_data: PostModel, db: SessionDep):
    return PostService.create_post(db, user_id, post_data)
    
    
    

@user_router.get("/{user_id}/posts", response_model=Posts)
async def user_posts(user_id: int, db: SessionDep, offset:int = 0, limit: int = 5, ):
    return PostService.get_posts(db, user_id, offset, limit)
    

    




