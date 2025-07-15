from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TestBase(BaseModel):
    tipo_prueba: str
    equipo_id: int

class TestCreate(TestBase):
    """Esquema para crear un Test"""
    pass

class TestOut(TestBase):
    """Esquema para devolver un Test en respuestas"""
    id: int
    fecha: datetime

    class Config:
        orm_mode = True
