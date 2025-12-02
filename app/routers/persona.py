from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.persona import PersonaCreate, PersonaUpdate, PersonaResponse
from app.services import persona_service

router = APIRouter(
    prefix="/personas",
    tags=["Personas Atendidas"]
)

@router.post(
    "/",
    response_model=PersonaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva persona atendida"
)
def crear_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    # Validar documento único
    if persona_service.get_persona_by_document(db, persona.numero_documento):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe persona con documento {persona.numero_documento}"
        )
    
    return persona_service.create_persona(db, persona)

@router.get(
    "/{persona_id}",
    response_model=PersonaResponse,
    summary="Obtener persona por ID"
)
def obtener_persona(
    persona_id: int = Path(..., gt=0, description="ID de la persona"),
    db: Session = Depends(get_db)
):
    persona = persona_service.get_persona(db, persona_id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Persona con ID {persona_id} no encontrada"
        )
    return persona

@router.get(
    "/",
    response_model=List[PersonaResponse],
    summary="Listar personas"
)
def listar_personas(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=100, description="Límite por página"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    search: Optional[str] = Query(None, description="Buscar por texto"),
    db: Session = Depends(get_db)
):
    return persona_service.get_personas(db, skip, limit, estado, search)

@router.patch(
    "/{persona_id}",
    response_model=PersonaResponse,
    summary="Actualizar persona"
)
def actualizar_persona(
    persona_id: int = Path(..., gt=0),
    persona_update: PersonaUpdate = ...,
    db: Session = Depends(get_db)
):
    persona = persona_service.update_persona(db, persona_id, persona_update)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Persona con ID {persona_id} no encontrada"
        )
    return persona

@router.delete(
    "/{persona_id}",
    status_code=status.HTTP_200_OK,
    summary="Desactivar persona"
)
def eliminar_persona(
    persona_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    if not persona_service.delete_persona(db, persona_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Persona con ID {persona_id} no encontrada"
        )
    return {"message": f"Persona {persona_id} desactivada exitosamente"}