from sqlalchemy import Column, Integer, String, Date, Enum, Text
from sqlalchemy.sql import func
from app.models.base import Base
import enum

class TipoDocumentoEnum(str, enum.Enum):
    V = "V"
    E = "E"
    P = "P"
    J = "J"

class SexoEnum(str, enum.Enum):
    M = "M"
    F = "F"
    O = "O"

class EstadoPersonaEnum(str, enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"

class PersonaAtendida(Base):
    __tablename__ = 'personas_atendidas'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tipo_documento = Column(Enum(TipoDocumentoEnum), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(Enum(SexoEnum), nullable=False)
    correo = Column(String(100), nullable=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(Text, nullable=True)
    contacto_emergencia = Column(String(100), nullable=True)
    alergias = Column(Text, nullable=True)
    antecedentes_resumen = Column(Text, nullable=True)
    estado = Column(Enum(EstadoPersonaEnum), default=EstadoPersonaEnum.ACTIVO, nullable=False)
    fecha_creacion = Column(Date, server_default=func.now())
    fecha_actualizacion = Column(Date, onupdate=func.now())
    
    def __repr__(self):
        return f"<PersonaAtendida {self.nombres} {self.apellidos}>"