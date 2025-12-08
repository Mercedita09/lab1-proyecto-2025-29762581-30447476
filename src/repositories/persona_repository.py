from sqlalchemy.orm import Session
# from src.models.persona import Persona  # TODO: cuando esté creado

def get_persona_by_id(db: Session, persona_id: int):
    # TODO: conectar con modelo Persona
    return None

def create_persona(db: Session, persona_data):
    # TODO: insertar en la tabla Persona
    # Ejemplo cuando el modelo esté listo:
    # nueva_persona = Persona(**persona_data.dict())
    # db.add(nueva_persona)
    # db.commit()
    # db.refresh(nueva_persona)
    # return nueva_persona
    return None

def update_persona(db: Session, persona_id: int, persona_data):
    # TODO: actualizar registro
    return None

def delete_persona(db: Session, persona_id: int):
    # TODO: eliminar registro
    return None
