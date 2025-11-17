from fastapi import APIRouter, Request, HTTPException
from controllers.auth_controller import AuthController

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.get('/login')
async def login(request: Request):
    """Redirige al flujo de autenticación de Google."""
    return await AuthController.login(request)

@router.get('/callback', name='auth_callback')
async def callback(request: Request):
    """Recibe la respuesta de Google y genera tokens + cookies."""
    try:
        return await AuthController.callback(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/refresh')
async def refresh(request: Request):
    """Genera un nuevo access_token usando el refresh_token."""
    return await AuthController.refresh(request)

@router.get("/session")
async def session(request: Request):
    """Verifica si hay sesión. Devuelve los datos del usuario autenticado."""
    return await AuthController.validate_session(request)

@router.post('/logout')
async def logout(request: Request):
    """Elimina cookies y cierra sesión."""
    return await AuthController.logout(request)
