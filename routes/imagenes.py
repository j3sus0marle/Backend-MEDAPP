from fastapi import APIRouter,File, UploadFile,status
from fastapi.responses import JSONResponse
import shutil
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(
    prefix="/imagenes",
    tags=["imagenes"],
    #dependencies=[Depends(AuthController.verify_token)] 
)


router.post("/subir")
async def subir_imagen(file: UploadFile = File(...)):
    file_path = f"imagenes/{file.filename}"
    try:
        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(file.file,buffer)    
        
        url = f"http://{os.getenv("HOST")}:{os.getenv("PORT")}/uploads/{file.filename}"
    
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