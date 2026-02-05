from urllib.parse import urlencode
import httpx
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi.concurrency import run_in_threadpool

from ..core.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

class GoogleOAuthService:
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"

    @staticmethod
    def get_auth_url() -> str:
        params = {
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent"
        }
        return f"{GoogleOAuthService.AUTH_URL}?{urlencode(params)}"

    @staticmethod
    async def exchange_code_for_token(code: str) -> dict:
        data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(GoogleOAuthService.TOKEN_URL, data=data)
            response.raise_for_status()
            return response.json()
        
    @staticmethod
    async def verify_id_token(token: str) -> dict:
        try:
            payload = await run_in_threadpool(id_token.verify_oauth2_token, token, requests.Request(), GOOGLE_CLIENT_ID)
            return dict(payload)
        except ValueError as e:
            raise ValueError("Invalid ID token") from e
    