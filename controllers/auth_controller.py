from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse  
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
import os
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv
import secrets
from database import users_collection
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

# función para crear tokens con datos de usuario y duración
def create_token(data: dict, expires_minutes: int):
    data = data.copy()
    data["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    return jwt.encode(data, JWT_SECRET, algorithm="HS256")

SESSIONS = {}

class AuthController:
    @staticmethod
    async def login(request: Request):
        redirect_uri = request.url_for('auth_callback')
        print(f"[auth] redirect_uri={redirect_uri}")
        return await oauth.google.authorize_redirect(request, redirect_uri, prompt='select_account')

    @staticmethod
    async def callback(request: Request):
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo') or await oauth.google.parse_id_token(request, token)
        
        # Buscar usuario en la base de datos por google_sub o email
        db_user = await AuthController.get_user_by_google_sub(user.get('sub'))
        if not db_user:
            db_user = await AuthController.get_user_by_email(user.get('email'))
        
        if not db_user:
            # Si el usuario no existe en la BD, crear uno nuevo con rol por defecto
            user_data = {
                'email': user.get('email'),
                'name': user.get('name'),
                'google_sub': user.get('sub'),
                'role': 'Estudiante',
                'is_active': True,
                'created_at': datetime.now(timezone.utc),
                'last_login': datetime.now(timezone.utc)
            }
            db_user = await AuthController.create_user(user_data)
        else:
            # Actualizar último login
            await AuthController.update_user_last_login(str(db_user['_id']))
        
        # Verificar si el usuario está activo
        if not db_user.get('is_active', True):
            raise HTTPException(status_code=403, detail="Usuario desactivado")
        
        # Crear JWT con datos incluyendo el rol
        payload = {
            'sub': user.get('sub'),
            'email': user.get('email'),
            'name': user.get('name'),
            'role': db_user.get('role', 'Estudiante'),
            'user_id': str(db_user['_id'])
        }
        
        access_token = create_token(payload, 15)
        refresh_token = create_token(payload, 60 * 24 * 7)
        session_token = secrets.token_urlsafe(32)
        SESSIONS[session_token] = {
            "user": payload, 
            "refresh_token": refresh_token,
            "db_user_id": str(db_user['_id'])
        }
        
        response = RedirectResponse(f"{FRONTEND_URL}/")
        response.set_cookie("access_token", access_token, httponly=True, samesite="lax", max_age=900)
        response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="lax", max_age=604800)
        response.set_cookie("session_token", session_token, httponly=True, samesite="lax", max_age=604800)
        
        return response
    
    @staticmethod
    def verify_token(request: Request):
        token = None

        if "access_token" in request.cookies:
            token = request.cookies.get("access_token")
        elif "Authorization" in request.headers:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
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
                    "name": payload.get("name"),
                    "role": payload.get("role"),
                    "user_id": payload.get("user_id")
                }
            })
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    @staticmethod
    async def refresh(request: Request):
        session_token = request.cookies.get("session_token")
        if not session_token or session_token not in SESSIONS:
            raise HTTPException(status_code=401, detail="Sesión inválida")
        
        session = SESSIONS[session_token]
        
        try:
            payload = jwt.decode(session["refresh_token"], JWT_SECRET, algorithms=["HS256"])
            
            # Verificar que el usuario aún existe y está activo
            db_user = await AuthController.get_user_by_email(payload.get('email'))
            if not db_user or not db_user.get('is_active', True):
                raise HTTPException(status_code=403, detail="Usuario no autorizado")
            
            # Actualizar el payload con datos actualizados de la BD
            payload['role'] = db_user.get('role', 'Estudiante')
            payload['user_id'] = str(db_user['_id'])
            
        except JWTError:
            raise HTTPException(status_code=401, detail="Refresh token inválido o expirado")
        
        new_access_token = create_token(payload, 15)
        new_refresh_token = create_token(payload, 60 * 24 * 7)
        session["refresh_token"] = new_refresh_token
        SESSIONS[session_token] = session
        
        response = JSONResponse({"access_token": new_access_token})
        response.set_cookie("access_token", new_access_token, httponly=True, samesite="lax", max_age=900)
        response.set_cookie("refresh_token", new_refresh_token, httponly=True, samesite="lax", max_age=604800)
        return response
    
    @staticmethod
    async def logout(request: Request):
        session_token = request.cookies.get("session_token")
        if session_token and session_token in SESSIONS:
            del SESSIONS[session_token]
        
        response = JSONResponse({"message": "Sesión cerrada"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.delete_cookie("session_token")
        return response

    @staticmethod
    # Función para verificar roles
    def require_role(required_role: str):
        
        async def role_dependency(request: Request):
            payload = AuthController.verify_token(request)
            user_role = payload.get('role')
            print(user_role)
            if user_role != required_role:
                raise HTTPException(
                status_code=403, 
                detail=f"Se requiere rol {required_role}. Tu rol actual es {user_role}"
                )
            return payload
        return role_dependency

    async def get_user_by_email(email: str):
        return await users_collection.find_one({"email": email})

    async def get_user_by_google_sub(google_sub: str):
        return await users_collection.find_one({"google_sub": google_sub})

    async def create_user(user_data: dict):
        result = await users_collection.insert_one(user_data)
        created_user = await users_collection.find_one({"_id": result.inserted_id})
        return created_user

    async def update_user_last_login(user_id: str):
        from bson import ObjectId
        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"last_login": datetime.now(timezone.utc)}} 
        )

    async def update_user_role(user_id: str, new_role: str):
        from bson import ObjectId
        result = await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"role": new_role}}
        )
        return result.modified_count > 0


        # Verificador específico para rol maestro
    @staticmethod
    def require_maestro(request: Request):
        return AuthController.require_role('Maestro')(request)