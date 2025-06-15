from pydantic import BaseModel
from typing import Optional

# Crear nuevo tipo de test
class TestCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

# Leer tipo de test
class TestOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

class Config:
    from_attributes = True

