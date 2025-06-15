from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Crear proyecto
class ProyectoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

# Leer proyecto
class ProyectoOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    fecha_creacion: Optional[datetime]

class Config:
    from_attributes = True

