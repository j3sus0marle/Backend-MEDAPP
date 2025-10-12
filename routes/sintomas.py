from fastapi import APIRouter, HTTPException
from typing import List
from controllers.sintomas_controller import SintomasController
from models.sintoma_model import Sintoma, SintomaCreate, SintomaUpdate

router = APIRouter(
    prefix="/sintomas",
    tags=["sintomas"],
)

@router.get("/", response_model=List[Sintoma])
async def get_sintomas():
    try:
        return await SintomasController.get_all_sintomas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/{sintoma_id}", response_model=Sintoma)
async def get_sintoma(sintoma_id: str):
    try:
        sintoma = await SintomasController.get_sintoma_by_id(sintoma_id)
        if sintoma:
            return sintoma
        raise HTTPException(status_code=404, detail="Síntoma no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"ID inválido: {str(e)}")

@router.post("/", response_model=Sintoma)
async def create_sintoma(sintoma: SintomaCreate):
    try:
        return await SintomasController.create_sintoma(sintoma.nombre)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.put("/{sintoma_id}", response_model=Sintoma)
async def update_sintoma(sintoma_id: str, sintoma_update: SintomaUpdate):
    try:
        sintoma = await SintomasController.update_sintoma(sintoma_id, sintoma_update.nombre)
        if sintoma:
            return sintoma
        raise HTTPException(status_code=404, detail="Síntoma no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")