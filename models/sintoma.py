from pydantic import BaseModel

class Sintoma(BaseModel):
    id: str
    numero: int
    nombre: str

class SintomaCreate(BaseModel):
    nombre: str  
    
class SintomaUpdate(BaseModel):
    nombre: str