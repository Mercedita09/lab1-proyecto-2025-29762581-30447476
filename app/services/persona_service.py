# app/services/persona_service.py
from sqlalchemy.orm import Session
from app.models.persona import PersonaAtendida
from app.schemas.persona import PersonaCreate
from typing import List

def get_persona_by_document(db: Session, doc_num: str):
    """Verifica la unicidad del documento (Regla de Negocio)."""
    return db.query(PersonaAtendida).filter(
        PersonaAtendida.numeroDocumento == doc_num
    ).first()

def get_persona(db: Session, persona_id: int):
    """Busca una persona por ID."""
    return db.query(PersonaAtendida).filter(
        PersonaAtendida.id == persona_id
    ).first()

def get_personas(db: Session, skip: int = 0, limit: int = 100) -> List[PersonaAtendida]:
    """Lista personas con paginación."""
    return db.query(PersonaAtendida).offset(skip).limit(limit).all()

def create_persona(db: Session, persona: PersonaCreate) -> PersonaAtendida:
    """Crea un nuevo registro de Persona Atendida."""
    # Nota: Aquí iría lógica de validación compleja, ej: si el paciente es menor 
    # de edad y no tiene contacto de emergencia, lanzar error.
    
    db_persona = PersonaAtendida(**persona.model_dump())
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

# Próximas Implementaciones (Ej. PATCH para cambiar estado)
# def deactivate_persona(db: Session, persona_id: int):
#     db_persona = get_persona(db, persona_id)
#     if db_persona:
#         db_persona.estado = 'inactivo'
#         db.commit()
#         db.refresh(db_persona)
#     return db_persona