from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.repositories.persona_repository import get_persona_by_id
from src.database import get_db  # Asumiendo que tienes un archivo para la sesión DB

router = APIRouter(prefix="/personas", tags=["Personas"])

@router.get("/{persona_id}")
def obtener_persona(persona_id: int, db: Session = Depends(get_db)):
    persona = get_persona_by_id(db, persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona
