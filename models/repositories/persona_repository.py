from sqlalchemy.orm import Session
from src.models.persona_model import Persona

def get_persona(db: Session, persona_id: int):
    return db.query(Persona).filter(Persona.id == persona_id).first()

def create_persona(db: Session, persona: Persona):
    db.add(persona)
    db.commit()
    db.refresh(persona)
    return persona

def update_persona(db: Session, persona_id: int, data: dict):
    persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if persona:
        for key, value in data.items():
            setattr(persona, key, value)
        db.commit()
        db.refresh(persona)
    return persona

def delete_persona(db: Session, persona_id: int):
    persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if persona:
        db.delete(persona)
        db.commit()
    return persona
