import jwt
from datetime import datetime, timedelta
from ..core.config import SECRET_KEY, EXPIRES_TIME, ALGORITHM

class AuthService:
    
    @staticmethod
    def create_access_token(data:dict) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=EXPIRES_TIME)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_access_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise
        except jwt.InvalidTokenError:
            raise