from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from pydantic_core import core_schema
from bson import ObjectId
from .paquete_info_model import PaqueteInformacionDB
from typing import Any

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


# --- Modelos auxiliares ---
class TerminoRelacionado(BaseModel):
    nombre: str
    tipo: str


# --- Modelos principales ---
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

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    @field_serializer("id")
    def serialize_id(self, v: PyObjectId, _info):
        return str(v)


class CampoInformativoDB_ID(CampoInformativoDB):
    info_pack_data: PaqueteInformacionDB

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    @field_serializer("id")
    def serialize_id(self, v: PyObjectId, _info):
        return str(v)