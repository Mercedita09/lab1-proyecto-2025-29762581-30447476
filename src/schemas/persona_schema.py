from pydantic import BaseModel
from datetime import date
from typing import Optional

class PersonaBase(BaseModel):
    nombre: str
    cedula: str
    fecha_nacimiento: date
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    activo: Optional[bool] = True

class PersonaCreate(PersonaBase):
    pass

class PersonaUpdate(PersonaBase):
    pass

class PersonaResponse(PersonaBase):
    id: int

    class Config:
        orm_mode = True
