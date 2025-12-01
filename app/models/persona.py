# app/models/persona.py
from sqlalchemy import Column, Integer, String, Date, Enum
from app.models.base import Base # Base es la clase base declarativa de SQLAlchemy

class PersonaAtendida(Base):
    """Corresponde a la entidad PersonasAtendidas (Pacientes) - Sección 2.1"""
    
    # 1. Nombre de la tabla en MySQL
    __tablename__ = 'PersonasAtendidas'

    # 2. Definición de las columnas
    id = Column(Integer, primary_key=True, index=True)
    tipoDocumento = Column(String(10), nullable=False)
    numeroDocumento = Column(String(20), unique=True, nullable=False, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fechaNacimiento = Column(Date, nullable=False)
    sexo = Column(Enum('M', 'F', 'Otro'), nullable=False)
    # ... otras columnas
    estado = Column(Enum('activo', 'inactivo'), default='activo', nullable=False)