from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from .paquete_info_model import PaqueteInformacionDB
# Helper para usar ObjectId en Pydantic

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if not ObjectId.is_valid(v):
            raise ValueError("ID inválido")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {
            "type": "string",
            "title": "ObjectId",
            "examples": ["64f9c5b6f0d3c8e123456789"]
        }
# ---- Modelos ----

class TerminoRelacionado(BaseModel):
    nombre: str
    tipo: str

class CampoInformativoBase(BaseModel):
    titulo: str
    terminos_relacionados: List[TerminoRelacionado] = []
    info_pack_id: Optional[PyObjectId] = Field(default=None, alias="info_pack_id")

class CampoInformativoCreate(CampoInformativoBase):
    pass

class CampoInformativoUpdate(BaseModel):
    titulo: Optional[str] = None
    terminos_relacionados: Optional[List[TerminoRelacionado]] = None
    info_pack_id: Optional[PyObjectId] = None

class CampoInformativoDB(CampoInformativoBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
        
    class Config:
        json_encoders = {ObjectId: str}
        validate_by_name = True
        
    
class CampoInformativoDB_ID(CampoInformativoDB):
    info_pack_data: PaqueteInformacionDB
        
    class Config:
        json_encoders = {ObjectId: str,PyObjectId: str}
        validate_by_name = True