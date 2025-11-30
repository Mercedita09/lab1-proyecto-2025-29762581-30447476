from src.models.persona import Persona  # cuando ella lo cree
from sqlalchemy.orm import Session

def get_persona_by_id(db: Session, persona_id: int):
    return db.query(Persona).filter(Persona.id == persona_id).first()
