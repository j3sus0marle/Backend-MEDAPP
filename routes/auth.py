from fastapi import APIRouter, Request, HTTPException
from controllers.auth_controller import AuthController

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.get('/login')
async def login(request: Request):
    return await AuthController.login(request)

@router.get('/callback', name='auth_callback')
async def callback(request: Request):
    try:
        return await AuthController.callback(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
