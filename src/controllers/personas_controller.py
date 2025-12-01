from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.repositories import persona_repository
from src.schemas.persona_schema import PersonaCreate, PersonaUpdate, PersonaResponse
from src.models.persona_model import Persona

router = APIRouter(prefix="/personas", tags=["personas"])

# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PersonaResponse)
def crear_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    nueva_persona = Persona(**persona.dict())
    return persona_repository.create_persona(db, nueva_persona)

@router.get("/{id}", response_model=PersonaResponse)
def obtener_persona(id: int, db: Session = Depends(get_db)):
    persona = persona_repository.get_persona(db, id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@router.put("/{id}", response_model=PersonaResponse)
def actualizar_persona(id: int, persona: PersonaUpdate, db: Session = Depends(get_db)):
    persona_actualizada = persona_repository.update_persona(db, id, persona.dict())
    if not persona_actualizada:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona_actualizada

@router.delete("/{id}")
def eliminar_persona(id: int, db: Session = Depends(get_db)):
    persona_eliminada = persona_repository.delete_persona(db, id)
    if not persona_eliminada:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return {"detail": "Persona eliminada correctamente"}
