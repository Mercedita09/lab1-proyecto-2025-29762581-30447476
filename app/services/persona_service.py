from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.persona import PersonaAtendida, EstadoPersonaEnum
from app.schemas.persona import PersonaCreate, PersonaUpdate
from typing import List, Optional

def get_persona_by_document(db: Session, numero_documento: str) -> Optional[PersonaAtendida]:
    """Busca una persona por número de documento."""
    return db.query(PersonaAtendida).filter(
        PersonaAtendida.numero_documento == numero_documento
    ).first()

def get_persona(db: Session, persona_id: int) -> Optional[PersonaAtendida]:
    """Busca una persona por ID."""
    return db.query(PersonaAtendida).filter(PersonaAtendida.id == persona_id).first()

def get_personas(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    estado: Optional[str] = None,
    search: Optional[str] = None
) -> List[PersonaAtendida]:
    """
    Obtiene lista de personas con paginación y filtros.
    
    Args:
        db: Sesión de base de datos
        skip: Número de registros a omitir (paginación)
        limit: Máximo número de registros a retornar
        estado: Filtrar por estado ('activo' o 'inactivo')
        search: Texto para buscar en nombres, apellidos o documento
    
    Returns:
        Lista de objetos PersonaAtendida ordenados por fecha de creación descendente
    """
    query = db.query(PersonaAtendida)
    
    # Aplicar filtro por estado si se proporciona
    if estado:
        query = query.filter(PersonaAtendida.estado == estado)
    
    # Aplicar búsqueda por texto si se proporciona
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                PersonaAtendida.nombres.ilike(search_term),
                PersonaAtendida.apellidos.ilike(search_term),
                PersonaAtendida.numero_documento.ilike(search_term)
            )
        )
    
    # Ordenar por fecha de creación descendente (más recientes primero)
    query = query.order_by(PersonaAtendida.fecha_creacion.desc())
    
    # Aplicar paginación
    return query.offset(skip).limit(limit).all()

def create_persona(db: Session, persona: PersonaCreate) -> PersonaAtendida:
    """Crea una nueva persona en la base de datos."""
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
    """
    Actualiza una persona existente.
    
    Args:
        db: Sesión de base de datos
        persona_id: ID de la persona a actualizar
        persona_update: Datos a actualizar (solo campos enviados)
    
    Returns:
        Persona actualizada o None si no existe
    """
    db_persona = get_persona(db, persona_id)
    if db_persona:
        # Solo actualiza los campos enviados en la solicitud
        update_data = persona_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_persona, field, value)
        db.commit()
        db.refresh(db_persona)
    return db_persona

def delete_persona(db: Session, persona_id: int) -> bool:
    """
    Eliminación lógica de una persona (cambia estado a inactivo).
    
    Args:
        db: Sesión de base de datos
        persona_id: ID de la persona a desactivar
    
    Returns:
        True si se desactivó, False si no se encontró
    """
    db_persona = get_persona(db, persona_id)
    if db_persona:
        db_persona.estado = EstadoPersonaEnum.INACTIVO
        db.commit()
        return True
    return False