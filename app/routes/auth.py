from fastapi import APIRouter, Depends
from ..schemas import UserOut, UserModel, LoginModel, TokenOut
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
from ..core.config import GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI
from ..services.google_auth_service import GoogleOAuthService

from ..services import UserService, get_user_service
from ..core.dependencies import get_current_user



auth_router = APIRouter(prefix = "/api/v1/auth")

@auth_router.post("/reg", response_model=UserOut,status_code=201)
async def create_user(data: UserModel, user_service: UserService = Depends(get_user_service)):
    return await user_service.create_user(data)

@auth_router.post("/login", response_model=TokenOut, status_code=200)
async def login(data: LoginModel, user_service: UserService = Depends(get_user_service)):
    return await user_service.login_user(data.username, data.password)

@auth_router.get("/google/login")
async def google_login():
    url = GoogleOAuthService.get_auth_url()
    return RedirectResponse(url)

@auth_router.get("/google/callback")
async def google_callback(code: str, user_service: UserService = Depends(get_user_service)):
    token_data = await GoogleOAuthService.exchange_code_for_token(code)
    user_info = await GoogleOAuthService.verify_id_token(token_data["id_token"])

    return await user_service.login_google_user(user_info)





