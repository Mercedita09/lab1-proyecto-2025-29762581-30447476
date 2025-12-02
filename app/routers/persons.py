from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.persona import PersonaCreate, PersonaUpdate, PersonaResponse
from app.services import persona_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/personas",
    tags=["Personas Atendidas"]
)

@router.post(
    "/",
    response_model=PersonaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva persona atendida",
    description="""
    Crea un nuevo registro de persona atendida (paciente) en el sistema.
    
    ## Validaciones:
    - Número de documento debe ser único en el sistema
    - Todos los campos obligatorios deben estar presentes
    - Validación automática de formato de email (si se provee)
    - Validación de formato de teléfono (si se provee)
    
    ## Campos obligatorios:
    - tipo_documento
    - numero_documento  
    - nombres
    - apellidos
    - fecha_nacimiento
    - sexo
    
    ## Respuesta exitosa (201):
    Retorna el objeto creado con su ID asignado.
    """
)
async def crear_persona(
    persona: PersonaCreate, 
    db: Session = Depends(get_db)
) -> PersonaResponse:
    """
    Endpoint para crear una nueva persona atendida.
    """
    logger.info(f"Creando nueva persona con documento: {persona.numero_documento}")
    
    # Validar que el documento no exista
    existente = persona_service.get_persona_by_document(db, persona.numero_documento)
    if existente:
        logger.warning(f"Documento duplicado: {persona.numero_documento}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "Documento duplicado",
                "message": f"Ya existe una persona con el documento {persona.numero_documento}",
                "persona_id": existente.id
            }
        )
    
    try:
        nueva_persona = persona_service.create_persona(db, persona)
        logger.info(f"Persona creada exitosamente - ID: {nueva_persona.id}")
        return nueva_persona
    except Exception as e:
        logger.error(f"Error creando persona: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al crear la persona"
        )

@router.get(
    "/{persona_id}",
    response_model=PersonaResponse,
    summary="Obtener persona por ID",
    description="Obtiene los datos completos de una persona atendida usando su ID único."
)
async def obtener_persona(
    persona_id: int = Path(..., gt=0, title="ID de la persona", description="ID numérico único de la persona"),
    db: Session = Depends(get_db)
) -> PersonaResponse:
    """
    Endpoint para obtener una persona por su ID.
    """
    logger.info(f"Buscando persona con ID: {persona_id}")
    
    persona = persona_service.get_persona(db, persona_id)
    if not persona:
        logger.warning(f"Persona no encontrada - ID: {persona_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Persona no encontrada",
                "message": f"No existe una persona con el ID {persona_id}"
            }
        )
    
    return persona

@router.get(
    "/documento/{numero_documento}",
    response_model=PersonaResponse,
    summary="Buscar persona por documento",
    description="Busca una persona usando su número de documento (cédula, pasaporte, etc.)."
)
async def buscar_por_documento(
    numero_documento: str = Path(..., title="Número de documento", description="Número de documento de la persona"),
    db: Session = Depends(get_db)
) -> PersonaResponse:
    """
    Endpoint para buscar una persona por número de documento.
    """
    logger.info(f"Buscando persona con documento: {numero_documento}")
    
    persona = persona_service.get_persona_by_document(db, numero_documento)
    if not persona:
        logger.warning(f"Persona no encontrada - Documento: {numero_documento}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Persona no encontrada",
                "message": f"No existe una persona con el documento {numero_documento}"
            }
        )
    
    return persona

@router.get(
    "/",
    response_model=List[PersonaResponse],
    summary="Listar personas atendidas",
    description="""
    Obtiene una lista paginada de personas atendidas con filtros opcionales.
    
    ## Parámetros de consulta:
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Máximo número de registros por página (1-100)
    - **estado**: Filtrar por estado ('activo' o 'inactivo')
    - **search**: Texto para buscar en nombres, apellidos o número de documento
    
    ## Ordenamiento:
    Los resultados se ordenan por fecha de creación descendente (más recientes primero).
    """
)
async def listar_personas(
    skip: int = Query(0, ge=0, description="Registros a omitir (paginación)"),
    limit: int = Query(100, ge=1, le=100, description="Límite de registros por página (máx. 100)"),
    estado: Optional[str] = Query(None, description="Filtrar por estado: 'activo' o 'inactivo'"),
    search: Optional[str] = Query(None, description="Texto para buscar en nombres, apellidos o documento"),
    db: Session = Depends(get_db)
) -> List[PersonaResponse]:
    """
    Endpoint para listar personas con paginación y filtros.
    """
    logger.info(f"Listando personas - skip: {skip}, limit: {limit}, estado: {estado}, search: {search}")
    
    personas = persona_service.get_personas(db, skip, limit, estado, search)
    logger.info(f"Encontradas {len(personas)} personas")
    
    return personas

@router.patch(
    "/{persona_id}",
    response_model=PersonaResponse,
    summary="Actualizar persona parcialmente",
    description="""
    Actualiza campos específicos de una persona existente.
    
    ## Características:
    - Solo actualiza los campos enviados en la solicitud
    - No permite cambiar el número de documento (es inmutable)
    - Permite cambiar el estado a 'inactivo' para desactivación lógica
    
    ## Campos actualizables:
    - correo
    - telefono  
    - direccion
    - contacto_emergencia
    - alergias
    - antecedentes_resumen
    - estado
    """
)
async def actualizar_persona(
    persona_id: int = Path(..., gt=0, description="ID de la persona a actualizar"),
    persona_update: PersonaUpdate = ...,
    db: Session = Depends(get_db)
) -> PersonaResponse:
    """
    Endpoint para actualizar parcialmente una persona.
    """
    logger.info(f"Actualizando persona ID: {persona_id}")
    
    persona = persona_service.update_persona(db, persona_id, persona_update)
    if not persona:
        logger.warning(f"Persona no encontrada para actualizar - ID: {persona_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Persona no encontrada",
                "message": f"No existe una persona con el ID {persona_id}"
            }
        )
    
    logger.info(f"Persona actualizada exitosamente - ID: {persona_id}")
    return persona

@router.delete(
    "/{persona_id}",
    status_code=status.HTTP_200_OK,
    summary="Desactivar persona",
    description="""
    Realiza una eliminación lógica de una persona cambiando su estado a 'inactivo'.
    
    ## Notas importantes:
    - No elimina físicamente el registro de la base de datos
    - Mantiene la integridad referencial con otros módulos
    - La persona puede ser reactivada actualizando su estado a 'activo'
    - El historial clínico y citas asociadas se mantienen
    """
)
async def eliminar_persona(
    persona_id: int = Path(..., gt=0, description="ID de la persona a desactivar"),
    db: Session = Depends(get_db)
) -> dict:
    """
    Endpoint para desactivar una persona (eliminación lógica).
    """
    logger.info(f"Desactivando persona ID: {persona_id}")
    
    if not persona_service.delete_persona(db, persona_id):
        logger.warning(f"Persona no encontrada para desactivar - ID: {persona_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Persona no encontrada",
                "message": f"No existe una persona con el ID {persona_id}"
            }
        )
    
    logger.info(f"Persona desactivada exitosamente - ID: {persona_id}")
    return {
        "success": True,
        "message": f"Persona {persona_id} desactivada exitosamente",
        "details": {
            "persona_id": persona_id,
            "action": "desactivacion_logica",
            "status": "inactivo"
        }
    }