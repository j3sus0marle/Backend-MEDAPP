from fastapi import APIRouter,File, HTTPException, UploadFile,status
from fastapi.responses import FileResponse, JSONResponse
import shutil
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(
    prefix="/imagenes",
    tags=["imagenes"],
    #dependencies=[Depends(AuthController.verify_token)] 
)


@router.post("/subir")
async def subir_imagen(file: UploadFile = File(...)):
    file_path = f"imagenes/{file.filename}"
    try:
        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(file.file,buffer)  
              
        host = os.getenv("HOST", "localhost")
        port = os.getenv("PORT", "8000")
        
        
        url = f"http://{host}:{port}/uploads/{file.filename}"
    
        return JSONResponse({
            "success": True,
            "url": url
        })
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": str(e)
            }
        )
        
@router.get("/ver/{nombre_imagen}")
async def ver_imagen(nombre_imagen: str):
    file_path = os.path.join("imagenes", nombre_imagen)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    return FileResponse(file_path)