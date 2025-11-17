from typing import List,Any, Optional
from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer, ConfigDict
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("ID inválido")
        return ObjectId(v)

# --- Modelos de contenido ---
class Texto(BaseModel):
    subtitulo: Optional[str] = None
    lugar: int
    texto: str

class Audio(BaseModel):
    titulo: Optional[str] = None
    lugar: int
    link: str

class Imagen(BaseModel):
    titulo: Optional[str] = None
    lugar: int
    link: str

class Video(BaseModel):
    titulo: Optional[str] = None
    lugar: int
    link: str

# --- Modelo principal del paquete ---
class PaqueteInformacionBase(BaseModel):
    textos: List[Texto] = []
    audios: List[Audio] = []
    imagenes: List[Imagen] = []
    videos: List[Video] = []

class PaqueteInformacionCreate(PaqueteInformacionBase):
    pass

class PaqueteInformacionDB(PaqueteInformacionBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,  # reemplaza a validate_by_name
        arbitrary_types_allowed=True  # permite tipos como ObjectId
    )

    # Serializador moderno (reemplaza json_encoders)
    @field_serializer("id")
    def serialize_objectid(self, v: PyObjectId, _info):
        return str(v)