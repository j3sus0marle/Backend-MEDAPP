from fastapi import FastAPI
from fastapi.responses import Response
from routes import sintomas

# Crear la aplicación FastAPI
app = FastAPI(
    title="Backend MEDAPP",
    description="API para aplicación médica",
    version="Prueba",
)

# Incluir las routes
app.include_router(sintomas.router)

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
            "sintomas": "/sintomas"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)