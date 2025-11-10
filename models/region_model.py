from typing import Optional, List, Any
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from pydantic_core import core_schema
from bson import ObjectId


# --- Helper para ObjectId ---
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


# --- Modelo de contenido individual ---
class ContenidoItem(BaseModel):
    tipo: str
    titulo: str
    info: str
    lugar: Optional[int] = None

class TerminoRelacionado(BaseModel):
    nombre: str 
    tipo: str 

# --- Modelo principal de respuesta ---
class RegionGET(BaseModel):
    region_name: str = Field(..., description="Nombre de la región (meshName)")
    titulo: str = Field(..., description="Título del campo informativo")
    contenido: List[ContenidoItem] = Field(default_factory=list, description="Lista de elementos multimedia ordenados por lugar")
    terminos_relacionados: List[TerminoRelacionado] = Field(default_factory=list, description="Lista de términos relacionados")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "region_name": "Cabeza",
                "titulo": "Anatomía de la cabeza",
                "contenido": [
                    {"tipo": "audio", "titulo": "Explicación general", "info": "https://audio.link/123", "lugar": 1},
                    {"tipo": "texto", "titulo": "Detalles anatómicos", "info": "El cráneo protege el cerebro.", "lugar": 2},
                    {"tipo": "video", "titulo": "Video ilustrativo", "info": "https://youtube.com/example", "lugar": 3}
                ],
                "terminos_relacionados": [
                    {"nombre": "Cráneo", "tipo": "Hueso"},
                    {"nombre": "Cerebro", "tipo": "Órgano"},
                    {"nombre": "Nervios craneales", "tipo": "Sistema"}
                ]
            }
        }
    )