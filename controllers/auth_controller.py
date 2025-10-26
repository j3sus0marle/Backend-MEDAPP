from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse  
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
import os
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET", "secret")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

oauth = OAuth()
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)
#funcion para crear tokens con datos de usuario y duracion
def create_token(data: dict, expires_minutes: int):
    data = data.copy()
    data["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    return jwt.encode(data,JWT_SECRET, algorithm="HS256")


class AuthController:
    @staticmethod
    async def login(request: Request):
        redirect_uri = request.url_for('auth_callback')
        print(f"[auth] redirect_uri={redirect_uri}")
        # Forzar selector de cuenta con prompt='select_account' para que el usuario pueda elegir
        return await oauth.google.authorize_redirect(request, redirect_uri, prompt='select_account')

    @staticmethod
    async def callback(request: Request):
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo') or await oauth.google.parse_id_token(request, token)
        # Crear JWT con algunos claims
        payload = {
            'sub': user.get('sub'),
            'email': user.get('email'),
            'name': user.get('name'),
        }
        access_token = create_token(payload, 15) # 15 minutos
        refresh_token =  create_token(payload, 60 * 24 * 7) # una semana
        response = RedirectResponse(f"{FRONTEND_URL}/")
        response.set_cookie("access_token", access_token, httponly=True, samesite="lax",max_age=900)
        response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="lax", max_age=604800)
        return response
    
    @staticmethod
    def verify_token(token: str):
       try:
           return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
       except JWTError:
           raise HTTPException(status_code=401,detail="Token inválido o expirado")
       
    @staticmethod
    async def refresh(request: Request):
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=401,detail="No hay refresh token")
        try:
            payload = jwt.decode(refresh_token,JWT_SECRET,algorithms=["HS256"])
        except JWTError:
            raise HTTPException(status_code=401, detail="Refresh token inválido o expirado")
        new_access_token = create_token(payload,15)
        response = JSONResponse({"access_token":new_access_token})
        response.set_cookie("access_token", new_access_token, httponly=True, samesite="lax", max_age=900)
        return response
    
    @staticmethod
    async def logout():
        response = JSONResponse({"message":"Sesion cerrada"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response