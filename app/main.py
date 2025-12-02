from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import persons
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja inicio y cierre de la aplicación."""
    logger.info("🚀 Iniciando API de Gestión de Servicios Médicos...")
    
    try:
        # Crear tablas en MySQL
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas creadas en MySQL")
    except Exception as e:
        logger.error(f"❌ Error creando tablas: {e}")
        raise
    
    yield
    
    logger.info("👋 Cerrando aplicación...")

# Crear aplicación FastAPI
app = FastAPI(
    title="API Gestión de Servicios Médicos",
    description="API REST para gestión de servicios de salud - Laboratorio I",
    version="1.0.0",
    docs_url="/api-docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(persons.router, prefix="/api/v1", tags=["Personas Atendidas"])

# Endpoints del sistema
@app.get("/", tags=["Sistema"])
def root():
    return {
        "message": "API de Gestión de Servicios Médicos",
        "version": "1.0.0",
        "database": "MySQL",
        "authors": [
            "Barbara Raquel Rincón Mújica - C.I.: 29762581",
            "Mercedes del Carmen Cordero Alvarez - C.I.: 30447476"
        ],
        "endpoints": {
            "personas": "/api/v1/personas",
            "documentación": "/api-docs",
            "health": "/health"
        }
    }

@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "healthy", "database": "MySQL"}

@app.get("/info", tags=["Sistema"])
def info():
    return {
        "proyecto": "Plataforma API para Gestión de Servicios Médicos",
        "asignatura": "Laboratorio I",
        "profesor": "Jonathan Falcon",
        "universidad": "Universidad Centroccidental 'Lisandro Alvarado'",
        "tecnologias": ["Python", "FastAPI", "MySQL", "SQLAlchemy", "Pydantic"]
    }