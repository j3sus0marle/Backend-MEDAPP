from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse  
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
import os
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv
import secrets

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

SESSIONS = {}

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
        session_token = secrets.token_urlsafe(32)
        SESSIONS[session_token] = {"user": payload, "refresh_token": refresh_token}
        
        response = RedirectResponse(f"{FRONTEND_URL}/")
        response.set_cookie("access_token", access_token, httponly=True, samesite="lax",max_age=900)
        response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="lax", max_age=604800)
        response.set_cookie("session_token", session_token, httponly=True, samesite="lax", max_age=604800)
        
        return response
    
    @staticmethod
    def verify_token(request: Request):
        token = None

        #access_token desde las cookies
        if "access_token" in request.cookies:
            token = request.cookies.get("access_token")

        #access_token desde el header Authorization
        elif "Authorization" in request.headers:
            auth_header = request.headers.get("Authorization")
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            raise HTTPException(status_code=401, detail="No se encontró el token de acceso")

        try:
            return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
       
    @staticmethod
    async def validate_session(request: Request):
        access_token = request.cookies.get("access_token")
        if not access_token:
            raise HTTPException(status_code=401, detail="No hay sesión activa")

        try:
            payload = jwt.decode(access_token, JWT_SECRET, algorithms=["HS256"])
            return JSONResponse({
                "session_active": True,
                "user": {
                    "email": payload.get("email"),
                    "name": payload.get("name")
                }
            })
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    @staticmethod
    async def refresh(request: Request):
        session_token = request.cookies.get("session_token")
        if not session_token or session_token not in SESSIONS:
            raise HTTPException(status_code=401,detail="Sesión inválida")
        session = SESSIONS[session_token]
        
        try:
            payload = jwt.decode(session["refresh_token"],JWT_SECRET, algorithms=["HS256"])
        except JWTError:
            raise HTTPException(status_code=401,detail="Refresh token inválido o expirado")
        new_access_token = create_token(payload, 15)
        session["refresh_token"] = create_token(payload, 60 * 24 * 7)
        SESSIONS[session_token] = session
        
        response = JSONResponse({"access_token": new_access_token})
        response.set_cookie("access_token", new_access_token, httponly=True, samesite="lax", max_age=900)
        response.set_cookie("refresh_token", session["refresh_token"], httponly=True, samesite="lax", max_age=604800)
        return response
    
    @staticmethod
    async def logout(request: Request):
        session_token = request.cookies.get("session_token")
        if session_token and session_token in SESSIONS:
            del SESSIONS[session_token]
        
        response = JSONResponse({"message":"Sesion cerrada"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.delete_cookie("session_token")
        return response