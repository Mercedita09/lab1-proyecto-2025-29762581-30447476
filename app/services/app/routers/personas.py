# app/routers/personas.py (ARCHIVO MODIFICADO)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.persona import PersonaCreate, PersonaResponse
from app.services import persona_service # Importar el servicio

router = APIRouter(
    prefix="/personas",
    tags=["2.1 Identidades - Personas Atendidas"]
)

# ----------------- Endpoints (Controladores) -----------------

@router.post("/", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
def alta_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    """[POST] Crea una nueva Persona Atendida (Paciente)."""
    
    # 1. Llamada al Servicio para validar unicidad (Lógica de Negocio)
    db_persona_existente = persona_service.get_persona_by_document(db, persona.numeroDocumento)
    if db_persona_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error: Ya existe una persona registrada con ese número de documento."
        )
    
    # 2. Llamada al Servicio para crear
    return persona_service.create_persona(db=db, persona=persona)

@router.get("/{persona_id}", response_model=PersonaResponse)
def consulta_persona(persona_id: int, db: Session = Depends(get_db)):
    """[GET] Consulta los datos de una persona por su ID."""
    
    db_persona = persona_service.get_persona(db, persona_id=persona_id) # Llamada al Servicio
    if db_persona is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Persona no encontrada"
        )
    return db_persona
    
@router.get("/", response_model=List[PersonaResponse])
def listar_personas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """[GET] Lista personas con paginación."""
    return persona_service.get_personas(db, skip=skip, limit=limit) # Llamada al Servicio