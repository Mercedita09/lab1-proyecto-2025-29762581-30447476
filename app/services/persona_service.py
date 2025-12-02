from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.persona import PersonaAtendida, EstadoPersonaEnum
from app.schemas.persona import PersonaCreate, PersonaUpdate
from typing import List, Optional

def get_persona_by_document(db: Session, numero_documento: str) -> Optional[PersonaAtendida]:
    return db.query(PersonaAtendida).filter(
        PersonaAtendida.numero_documento == numero_documento
    ).first()

def get_persona(db: Session, persona_id: int) -> Optional[PersonaAtendida]:
    return db.query(PersonaAtendida).filter(PersonaAtendida.id == persona_id).first()

def get_personas(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    estado: Optional[str] = None,
    search: Optional[str] = None
) -> List[PersonaAtendida]:
    query = db.query(PersonaAtendida)
    
    if estado:
        query = query.filter(PersonaAtendida.estado == estado)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                PersonaAtendida.nombres.ilike(search_term),
                PersonaAtendida.apellidos.ilike(search_term),
                PersonaAtendida.numero_documento.ilike(search_term)
            )
        )
    
    return query.offset(skip).limit(limit).all()

def create_persona(db: Session, persona: PersonaCreate) -> PersonaAtendida:
    db_persona = PersonaAtendida(**persona.model_dump())
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

def update_persona(
    db: Session, 
    persona_id: int, 
    persona_update: PersonaUpdate
) -> Optional[PersonaAtendida]:
    db_persona = get_persona(db, persona_id)
    if db_persona:
        update_data = persona_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_persona, field, value)
        db.commit()
        db.refresh(db_persona)
    return db_persona

def delete_persona(db: Session, persona_id: int) -> bool:
    db_persona = get_persona(db, persona_id)
    if db_persona:
        db_persona.estado = EstadoPersonaEnum.INACTIVO
        db.commit()
        return True
    return False