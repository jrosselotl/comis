from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ResultadoMegadoSchema(BaseModel):
    punto: str
    resultado_valor: Optional[float]
    unidad: str
    tiempo_aplicado: Optional[float] = None  # 🔹 Ahora lo ingresa el técnico manualmente
    observaciones: Optional[str] = None
    imagen: Optional[str] = None
    cable_set: Optional[int] = None

class TestMegadoSchema(BaseModel):
    equipo_id: int
    usuario_id: int
    test_id: int
    fecha: Optional[datetime] = None
    resultados: List[ResultadoMegadoSchema]

    class Config:
        orm_mode = True
