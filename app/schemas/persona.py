from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional
from enum import Enum

class TipoDocumentoEnum(str, Enum):
    V = "V"
    E = "E"
    P = "P"
    J = "J"

class SexoEnum(str, Enum):
    M = "M"
    F = "F"
    O = "O"

class EstadoPersonaEnum(str, Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"

class PersonaBase(BaseModel):
    tipo_documento: TipoDocumentoEnum
    numero_documento: str = Field(..., min_length=1, max_length=20)
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    fecha_nacimiento: date
    sexo: SexoEnum
    correo: Optional[str] = Field(None, max_length=100)  # Cambiado de EmailStr
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = None
    contacto_emergencia: Optional[str] = Field(None, max_length=100)
    alergias: Optional[str] = None
    antecedentes_resumen: Optional[str] = None

class PersonaCreate(PersonaBase):
    pass

class PersonaUpdate(BaseModel):
    correo: Optional[str] = None  # Cambiado de EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    contacto_emergencia: Optional[str] = None
    alergias: Optional[str] = None
    antecedentes_resumen: Optional[str] = None
    estado: Optional[EstadoPersonaEnum] = None

class PersonaResponse(PersonaBase):
    id: int
    estado: EstadoPersonaEnum
    fecha_creacion: date
    
    class Config:
        from_attributes = True