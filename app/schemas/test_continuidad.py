from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ResultadoContinuidadSchema(BaseModel):
    punto: str
    cable_set: Optional[int]
    resultado_valor: Optional[float]
    unidad: str
    observaciones: Optional[str]
    imagen: Optional[str]

class TestContinuidadSchema(BaseModel):
    equipo_id: int
    usuario_id: int
    test_id: int
    fecha: Optional[datetime] = None
    resultados: List[ResultadoContinuidadSchema]
