from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from typing import List
from controllers.campo_info_controller import CampoInfoController
from controllers.auth_controller import AuthController
from models.info_camp_model import CampoInformativoDB_ID,CampoInformativoDB, CampoInformativoCreate, CampoInformativoUpdate

router = APIRouter(
    prefix="/campos_info",
    tags=["campos_info"],
    dependencies=[Depends(AuthController.verify_token)] 
    
)

# ---- GET todos los campos ----
@router.get("/", response_model=List[CampoInformativoDB])
async def get_campos():
    try:
        return await CampoInfoController.get_all_campos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ---- GET por id ----
@router.get("/{campo_id}", response_model=CampoInformativoDB_ID)
async def get_campo(campo_id: str):
    try:
        campo = await CampoInfoController.get_campo_by_id(campo_id)
        if campo:
            return campo
        raise HTTPException(status_code=404, detail="Campo informativo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"ID inválido: {str(e)}")

# ---- POST crear nuevo campo ----
@router.post("/", response_model=CampoInformativoDB)
async def create_campo(campo: CampoInformativoCreate):
    try:
        return await CampoInfoController.create_campo(
            titulo=campo.titulo,
            terminos_relacionados=[tr.model_dump() for tr in campo.terminos_relacionados],
            info_pack_id=str(campo.info_pack_id) if campo.info_pack_id else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ---- PUT actualizar campo ----
@router.put("/{campo_id}", response_model=CampoInformativoDB)
async def update_campo(campo_id: str, campo_update: CampoInformativoUpdate):
    try:
        campo = await CampoInfoController.update_campo(
            campo_id=campo_id,
            titulo=campo_update.titulo,
            terminos_relacionados=campo_update.terminos_relacionados,
            info_pack_id=str(campo_update.info_pack_id) if campo_update.info_pack_id else None
        )
        if campo:
            return campo
        raise HTTPException(status_code=404, detail="Campo informativo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

# ---- DELETE eliminar campo ----
@router.delete("/{campo_id}")
async def delete_campo(campo_id: str):
    try:
        deleted = await CampoInfoController.delete_campo(campo_id)
        if deleted:
            return {"detail": "Campo informativo eliminado correctamente"}
        raise HTTPException(status_code=404, detail="Campo informativo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")