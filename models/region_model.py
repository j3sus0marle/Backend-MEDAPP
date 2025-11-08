from typing import Optional, Any
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


# --- Modelos principales ---
class RegionBase(BaseModel):
    meshName: str
    info_camp_id: Optional[PyObjectId] = Field(default=None, alias="info_camp_id")


class RegionCreate(RegionBase):
    """Modelo para crear un documento Mesh."""
    pass


class RegionUpdate(BaseModel):
    """Modelo para actualizar un documento Mesh."""
    meshName: Optional[str] = None
    info_camp_id: Optional[PyObjectId] = None


class RegionDB(RegionBase):
    """Modelo de lectura/escritura desde MongoDB."""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    @field_serializer("id")
    def serialize_id(self, v: PyObjectId, _info):
        return str(v)