from pydantic import BaseModel
from typing import Optional
from datetime import date

class PersonaBase(BaseModel):
    nombre: str
    cedula: str
    fecha_nacimiento: date
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None

class PersonaCreate(PersonaBase):
    pass

class PersonaUpdate(PersonaBase):
    activo: Optional[bool] = True

class PersonaOut(PersonaBase):
    id: int
    activo: bool

    class Config:
        orm_mode = True
