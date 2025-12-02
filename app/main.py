from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import persons
import logging
import time
from typing import Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja eventos de inicio y cierre de la aplicación."""
    startup_time = time.time()
    logger.info("🚀 Iniciando API de Gestión de Servicios Médicos...")
    
    try:
        # Crear tablas en MySQL (solo en desarrollo)
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas creadas/verificadas en MySQL")
    except Exception as e:
        logger.error(f"❌ Error creando tablas: {e}")
        # No raise para permitir que la app corra incluso si hay error de BD
        logger.warning("Continuando sin verificación de tablas...")
    
    startup_duration = time.time() - startup_time
    logger.info(f"✅ Aplicación lista en {startup_duration:.2f} segundos")
    
    yield
    
    logger.info("👋 Cerrando aplicación...")

# Crear aplicación FastAPI
app = FastAPI(
    title="API Gestión de Servicios Médicos - Laboratorio I",
    description="""
    ## 📋 Descripción
    API REST para la gestión integral de servicios de salud.
    
    ## 👥 Autores
    - **Barbara Raquel Rincón Mújica** - C.I.: 29762581
    - **Mercedes del Carmen Cordero Alvarez** - C.I.: 30447476
    
    ## 🏫 Información Académica
    - **Asignatura**: Laboratorio I
    - **Profesor**: Jonathan Falcon
    - **Universidad**: Universidad Centroccidental "Lisandro Alvarado"
    
    ## 🔧 Tecnologías
    - Python 3.9+
    - FastAPI
    - MySQL 8.0
    - SQLAlchemy
    - Pydantic
    
    ## 📚 Módulos Implementados
    - ✅ Personas Atendidas (CRUD completo)
    """,
    version="1.0.0",
    contact={
        "name": "Equipo Laboratorio I",
        "url": "https://github.com/tu-usuario/lab1-proyecto-2025-29762581-30447476",
    },
    docs_url="/api-docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Middleware de logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para loggear todas las requests."""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    # Calcular duración
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log response
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    
    return response

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: ["http://localhost:3000", "https://tudominio.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"]
)

# Manejo global de excepciones de validación
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Maneja errores de validación de Pydantic."""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Maneja excepciones generales no capturadas."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Error interno del servidor",
            "message": str(exc)
        },
    )

# Incluir routers
app.include_router(persons.router, prefix="/api/v1", tags=["Personas Atendidas"])

# Endpoints del sistema
@app.get("/", tags=["Sistema"])
async def root() -> Dict[str, Any]:
    """Endpoint raíz con información de la API."""
    return {
        "message": "Bienvenido a la API de Gestión de Servicios Médicos",
        "version": "1.0.0",
        "status": "operacional",
        "database": "MySQL 8.0",
        "authors": [
            {
                "nombre": "Barbara Raquel Rincón Mújica",
                "cedula": "29762581",
                "rol": "Controllers, Tests, Services"
            },
            {
                "nombre": "Mercedes del Carmen Cordero Alvarez",
                "cedula": "30447476",
                "rol": "Models, Services, Docs"
            }
        ],
        "documentation": {
            "swagger": "/api-docs",
            "redoc": "/redoc",
            "openapi_spec": "/openapi.json"
        },
        "endpoints_principales": [
            {"personas": "/api/v1/personas"},
            {"health": "/health"},
            {"info": "/info"}
        ]
    }

@app.get("/health", tags=["Sistema"])
async def health_check() -> Dict[str, Any]:
    """Health check para monitoreo del servicio."""
    from app.database import SessionLocal
    from sqlalchemy import text
    
    db_status = "unknown"
    try:
        # Verificar conexión a base de datos
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_status = "connected"
    except Exception as e:
        logger.error(f"Health check DB error: {e}")
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "api-gestion-servicios-medicos",
        "version": "1.0.0",
        "database": db_status,
        "environment": "development"
    }

@app.get("/info", tags=["Sistema"])
async def info() -> Dict[str, Any]:
    """Información técnica detallada de la API."""
    import sys
    import platform
    
    return {
        "proyecto": "Plataforma API para Gestión de Servicios Médicos",
        "descripcion": "Sistema para gestión integral de servicios de salud",
        "version": "1.0.0",
        "entorno": "development",
        "tecnologias": {
            "framework": "FastAPI",
            "orm": "SQLAlchemy 2.0",
            "validacion": "Pydantic 2.0",
            "base_datos": "MySQL 8.0",
            "driver": "PyMySQL"
        },
        "sistema": {
            "python": sys.version,
            "plataforma": platform.platform(),
            "arquitectura": platform.machine()
        },
        "estadisticas": {
            "endpoints": 7,
            "modelos": 1,
            "schemas": 3,
            "servicios": 1
        },
        "academico": {
            "asignatura": "Laboratorio I",
            "profesor": "Jonathan Falcon",
            "universidad": "Universidad Centroccidental 'Lisandro Alvarado'",
            "semestre": "2025-2"
        }
    }