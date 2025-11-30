from fastapi import FastAPI
from src.controllers import personas_controller

app = FastAPI()

# Endpoint de prueba para verificar que la API está viva
@app.get("/health")
def healthcheck():
    return {"status": "ok"}

# Registrar el router de personas
app.include_router(personas_controller.router)
