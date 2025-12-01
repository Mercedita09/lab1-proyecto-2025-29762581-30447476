from fastapi import FastAPI
from src.database import engine, Base
from src.controllers import personas_controller

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir el router de personas
app.include_router(personas_controller.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
