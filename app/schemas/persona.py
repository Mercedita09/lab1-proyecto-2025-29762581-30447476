from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date
from typing import Optional
from enum import Enum
import re

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
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = None
    contacto_emergencia: Optional[str] = Field(None, max_length=100)
    alergias: Optional[str] = None
    antecedentes_resumen: Optional[str] = None
    
    @validator('telefono')
    def validar_telefono(cls, v):
        if v and not re.match(r'^\+?[0-9\s\-\(\)]{7,20}$', v):
            raise ValueError('Formato de teléfono inválido')
        return v

class PersonaCreate(PersonaBase):
    pass

class PersonaUpdate(BaseModel):
    correo: Optional[EmailStr] = None
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