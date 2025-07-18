from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ResultadoTorqueSchema(BaseModel):
    cable_set: Optional[int] = None
    punto_prueba: str
    valor_nominal: Optional[float] = None
    valor_comprobacion: Optional[float] = None  # 🔹 Nombre alineado con el modelo y rutas
    resultado_valor: Optional[float] = None
    unidad: Optional[str] = None
    observaciones: Optional[str] = None
    imagen: Optional[str] = None

class TestTorqueSchema(BaseModel):
    equipo_id: int
    usuario_id: Optional[int] = None
    test_id: Optional[int] = None
    fecha: Optional[datetime] = None
    resultados: List[ResultadoTorqueSchema]

    class Config:
        orm_mode = True
