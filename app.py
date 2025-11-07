from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
from routes import campos_info, auth, paquetes_info

load_dotenv()


# Crear la aplicación FastAPI
app = FastAPI(
    title="Backend MEDAPP",
    description="API para aplicación médica",
    version="Prueba",
)

#(Google OAuth)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "una_clave_segura_y_larga")  # Usa una clave real y secreta
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://tu-frontend.vercel.app",  # Reemplaza con tu dominio de frontend
        "https://*.vercel.app"  # Permite todos los subdominios de vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(campos_info.router) # Endpoints protegidos (CRUD)
app.include_router(paquetes_info.router)
app.include_router(auth.router)

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
            "campos_info":"/campos_info",
            "paquete_info":"/paquete_info",
            "auth_login": "/auth/login"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)