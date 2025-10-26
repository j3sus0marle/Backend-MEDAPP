from typing import List
from pydantic import BaseModel, Field
from bson import ObjectId

# Helper para ObjectId en Pydantic
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

# ---- Modelos de contenido ----
class Texto(BaseModel):
    subtitulo: str
    lugar: int
    texto: str

class Audio(BaseModel):
    titulo: str
    lugar: int
    link: str

class Imagen(BaseModel):
    titulo: str
    lugar: int
    link: str

class Video(BaseModel):
    titulo: str
    lugar: int
    link: str

# ---- Modelo principal del paquete ----
class PaqueteInformacionBase(BaseModel):
    textos: List[Texto] = []
    audios: List[Audio] = []
    imagenes: List[Imagen] = []
    videos: List[Video] = []

class PaqueteInformacionCreate(PaqueteInformacionBase):
    pass

class PaqueteInformacionDB(PaqueteInformacionBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str, PyObjectId: str}
        validate_by_name = True