from fastapi import APIRouter, HTTPException, Depends
from typing import List
from controllers.paquete_info_controller import PaqueteInfoController
from controllers.auth_controller import AuthController
from models.paquete_info_model import PaqueteInformacionDB, PaqueteInformacionCreate

router = APIRouter(
    prefix="/paquetes_info",
    tags=["paquetes_info"],
    #dependencies=[Depends(AuthController.verify_token)]
)

# ---- GET todos los paquetes ----
@router.get("/", response_model=List[PaqueteInformacionDB])
async def get_paquetes():
    """Regresa todos los paquetes de información."""
    try:
        return await PaqueteInfoController.get_all_packs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ---- GET paquete por id ----
@router.get("/{pack_id}", response_model=PaqueteInformacionDB)
async def get_paquete(pack_id: str):
    """Regresa un paquete de información en particular por ID."""
    try:
        pack = await PaqueteInfoController.get_pack_by_id(pack_id)
        if pack:
            return pack
        raise HTTPException(status_code=404, detail="Paquete de información no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"ID inválido: {str(e)}")

# ---- POST crear nuevo paquete ----
@router.post("/", response_model=PaqueteInformacionDB)
async def create_paquete(pack: PaqueteInformacionCreate):
    """Permite crear un nuevo paquete de información."""
    try:
        return await PaqueteInfoController.create_pack(
            textos=pack.textos,
            audios=pack.audios,
            imagenes=pack.imagenes,
            videos=pack.videos
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ---- PUT actualizar paquete ----
@router.put("/{pack_id}", response_model=PaqueteInformacionDB)
async def update_paquete(pack_id: str, pack_update: PaqueteInformacionDB):
    """Permite actualizar un paquete de información existente."""
    try:
        updated_pack = await PaqueteInfoController.update_pack(
            pack_id, 
            textos=pack_update.textos,
            audios=pack_update.audios,
            imagenes=pack_update.imagenes,
            videos=pack_update.videos
        )
        if updated_pack:
            return updated_pack
        raise HTTPException(status_code=404, detail="Paquete de información no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

# ---- DELETE eliminar paquete ----
@router.delete("/{pack_id}")
async def delete_paquete(pack_id: str):
    """Elimina un paquete de información por ID."""
    try:
        deleted = await PaqueteInfoController.delete_pack(pack_id)
        if deleted:
            return {"detail": "Paquete de información eliminado correctamente"}
        raise HTTPException(status_code=404, detail="Paquete de información no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")