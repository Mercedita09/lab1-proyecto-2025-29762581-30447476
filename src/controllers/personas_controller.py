from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.persona_schema import PersonaCreate, PersonaUpdate, PersonaOut
from src.repositories import persona_repository
from src.database import get_db  # TODO: cuando esté creado

router = APIRouter(prefix="/personas", tags=["Personas"])

# Endpoint GET /personas/{id}
@router.get("/{persona_id}", response_model=PersonaOut)
def obtener_persona(persona_id: int, db: Session = Depends(get_db)):
    persona = persona_repository.get_persona_by_id(db, persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

# Endpoint POST /personas
@router.post("/", response_model=PersonaOut)
def crear_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    nueva_persona = persona_repository.create_persona(db, persona)
    if not nueva_persona:
        raise HTTPException(status_code=400, detail="No se pudo crear la persona")
    return nueva_persona

# Endpoint PUT /personas/{id}
@router.put("/{persona_id}", response_model=PersonaOut)
def actualizar_persona(persona_id: int, persona: PersonaUpdate, db: Session = Depends(get_db)):
    persona_actualizada = persona_repository.update_persona(db, persona_id, persona)
    if not persona_actualizada:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona_actualizada

# Endpoint DELETE /personas/{id}
@router.delete("/{persona_id}")
def eliminar_persona(persona_id: int, db: Session = Depends(get_db)):
    eliminado = persona_repository.delete_persona(db, persona_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return {"detail": "Persona eliminada correctamente"}
