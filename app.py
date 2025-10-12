from fastapi import FastAPI
from fastapi.responses import Response
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
from routes import sintomas
from routes import auth

load_dotenv()

# Secret para SessionMiddleware (usa la variable de entorno o una por defecto)
SESSION_SECRET = os.getenv('SESSION_SECRET', os.getenv('JWT_SECRET', 'super-secret-session-key'))

# Crear la aplicación FastAPI
app = FastAPI(
    title="Backend MEDAPP",
    description="API para aplicación médica",
    version="Prueba",
)

# Incluir las routes
app.include_router(sintomas.router)
app.include_router(auth.router)

# Agregar middleware de sesión necesario para authlib
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Evitar error 404 del favicon"""
    return Response(status_code=204)

@app.get("/")
def read_root():
    """Endpoint principal - Bienvenida a la API"""
    return {
        "message": "¡Bienvenido a Backend MEDAPP!",
        "version": "Prueba",
        "docs": "/docs",
        "endpoints": {
            "sintomas": "/sintomas",
            "auth_login": "/auth/login"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)