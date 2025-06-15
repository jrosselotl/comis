from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Resultado individual
class ResultadoContinuidadBase(BaseModel):
    punto_prueba: str
    referencia_valor: Optional[str]
    resultado_valor: Optional[str]
    aprobado: bool
    imagen_url: Optional[str] = None

class ResultadoContinuidadCreate(ResultadoContinuidadBase):
    pass

class ResultadoContinuidadOut(ResultadoContinuidadBase):
    id: int

    class Config:
        orm_mode = True

# Test principal
class TestContinuidadCreate(BaseModel):
    equipo_id: int
    usuario_id: int
    observaciones: Optional[str] = None
    resultados: List[ResultadoContinuidadCreate]

class TestContinuidadOut(BaseModel):
    id: int
    equipo_id: int
    usuario_id: int
    fecha: datetime
    observaciones: Optional[str]
    resultados: List[ResultadoContinuidadOut]
class Config:
        from_attributes = True  # Reemplaza cualquier 'orm_mode = True'