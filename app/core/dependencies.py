from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..services.auth_service import AuthService
from ..database import SessionDep
from ..services.user_service import UserService, get_user_service


security = HTTPBearer()


def get_current_user(user_service: UserService = Depends(get_user_service), bearer: HTTPAuthorizationCredentials = Depends(security)):
    token = bearer.credentials
    payload = AuthService.verify_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise
    return user_service.get_user_by_id(user_id)

      
    