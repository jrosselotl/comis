from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Resultado individual
class ResultadoMegadoBase(BaseModel):
    punto_prueba: str
    referencia_valor: Optional[str]
    resultado_valor: Optional[str]
    aprobado: bool
    imagen_url: Optional[str] = None

class ResultadoMegadoCreate(ResultadoMegadoBase):
    pass

class ResultadoMegadoOut(ResultadoMegadoBase):
    id: int

    class Config:
        orm_mode = True

# Test principal
class TestMegadoCreate(BaseModel):
    equipo_id: int
    usuario_id: int
    observaciones: Optional[str] = None
    resultados: List[ResultadoMegadoCreate]

class TestMegadoOut(BaseModel):
    id: int
    equipo_id: int
    usuario_id: int
    fecha: datetime
    observaciones: Optional[str]
    resultados: List[ResultadoMegadoOut]
class Config:
        from_attributes = True  # Reemplaza cualquier 'orm_mode = True'