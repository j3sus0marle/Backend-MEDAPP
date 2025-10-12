from authlib.integrations.starlette_client import OAuth
from fastapi import Request
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET", "secret")

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
            'name': user.get('name')
        }
        access_token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        return {'access_token': access_token, 'user': payload}
