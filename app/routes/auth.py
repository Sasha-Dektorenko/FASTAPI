from fastapi import APIRouter, Depends
from ..schemas import UserOut, UserModel
from ..database import SessionDep
from ..services import UserService, get_user_service


auth_router = APIRouter(prefix = "/api/v1/auth")

@auth_router.post("/reg", response_model=UserOut,status_code=201)
async def create_user(data: UserModel, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(data)