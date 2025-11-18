from fastapi import APIRouter, HTTPException, Depends
from typing import List
from controllers.campo_info_controller import CampoInfoController
from controllers.auth_controller import AuthController
from models.campo_info_model import CampoInformativoDB, CampoInformativoCreate, CampoInformativoUpdate

router = APIRouter(
    prefix="/campos_info",
    tags=["campos_info"],
    dependencies=[Depends(AuthController.verify_token)] 
)

@router.get("/", response_model=List[CampoInformativoDB])
async def get_campos():
    """Regresa todos los campos informativos."""
    try:
        return await CampoInfoController.get_all_campos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/{campo_id}", response_model=CampoInformativoDB)
async def get_campo(campo_id: str):
    """Regresa un campo informativo en particular, usando campo_id."""
    try:
        campo = await CampoInfoController.get_campo_by_id(campo_id)
        if campo:
            return campo
        raise HTTPException(status_code=404, detail="Campo informativo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"ID inválido: {str(e)}")

@router.post("/", response_model=CampoInformativoDB)
async def create_campo(
    campo: CampoInformativoCreate,
    user_data: dict = Depends(AuthController.require_role('Maestro'))  # Solo maestros pueden crear
):
    """Permite crear un nuevo campo informativo, para agregar en la base de datos."""
    try:
        return await CampoInfoController.create_campo(
            titulo=campo.titulo,
            terminos_relacionados=[tr.model_dump() for tr in campo.terminos_relacionados],
            info_pack_id=str(campo.info_pack_id) if campo.info_pack_id else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.put("/{campo_id}", response_model=CampoInformativoDB)  
async def update_campo(
    campo_id: str, 
    campo_update: CampoInformativoUpdate,
    user_data: dict = Depends(AuthController.require_role('maestro'))  # Solo maestros pueden actualizar
):
    """ Permite realizar algun cambio a un campo informativo."""
    try:
        campo = await CampoInfoController.update_campo(
            campo_id=campo_id,
            titulo=campo_update.titulo,
            terminos_relacionados=[tr.model_dump() for tr in campo_update.terminos_relacionados],
            info_pack_id=str(campo_update.info_pack_id) if campo_update.info_pack_id else None
        )
        if campo:
            return campo
        raise HTTPException(status_code=404, detail="Campo informativo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@router.delete("/{campo_id}")
async def delete_campo(
    campo_id: str,
    user_data: dict = Depends(AuthController.require_role('maestro'))  # Solo maestros pueden eliminar
):
    """Elimina un campo informativo de la base de datos, usando campo_id."""
    try:
        deleted = await CampoInfoController.delete_campo(campo_id)
        if deleted:
            return {"detail": "Campo informativo eliminado correctamente"}
        raise HTTPException(status_code=404, detail="Campo informativo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")