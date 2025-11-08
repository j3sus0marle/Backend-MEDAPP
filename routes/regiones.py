from fastapi import APIRouter, HTTPException, Depends
from typing import List
from controllers.region_controller import RegionController
from controllers.auth_controller import AuthController
from models.region_model import RegionDB
router = APIRouter(
    prefix="/regiones",
    tags=["regiones"],
    dependencies=[Depends(AuthController.verify_token)] 
)

@router.get("/{mesh_name}", response_model=RegionDB)
async def get_region_info(mesh_name: str):
    """
    Obtener información médica de una región del cuerpo por su meshName
    Para usar con el modelo 3D del frontend - Sin autenticación requerida
    """
    try:
        return await RegionController.get_region_by_mesh_name(mesh_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/health/status")
async def health_check():
    """Verificar estado de la base de datos - Sin autenticación requerida"""
    try:
        return await RegionController.health_check()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
