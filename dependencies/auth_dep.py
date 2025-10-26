from fastapi import Request, HTTPException, status
from jose import JWTError
from controllers.auth_controller import AuthController

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token and "authorization" in request.headers:
        header = request.headers["authorization"]
        if header.startswith("Bearer "):
            token = header.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="Token no encontrado")

    try:
        user = AuthController.verify_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    return user