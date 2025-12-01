from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de la base de datos (SQLite para pruebas, puede cambiarse a PostgreSQL/MySQL)
DATABASE_URL = "sqlite:///./personas.db"

# Motor de conexión
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Sesión de trabajo
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()
