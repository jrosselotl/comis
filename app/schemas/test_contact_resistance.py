from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ResultadoContactResistanceSchema(BaseModel):
    cable_set: Optional[int]
    punto_prueba: str
    resultado_valor: Optional[float]
    unidad: Optional[str]
    observaciones: Optional[str]
    imagen: Optional[str]

class TestContactResistanceSchema(BaseModel):
    proyecto_id: int
    equipo_id: int
    usuario_id: Optional[int] = None
    test_id: Optional[int] = None
    fecha: Optional[datetime] = None
    resultados: List[ResultadoContactResistanceSchema]

    class Config:
        orm_mode = True
