from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResultadoTorqueBase(BaseModel):
    cable_set: int
    punto_prueba: str
    valor_nominal: float
    valor_comprobado: Optional[float]
    aprobado: Optional[bool] = False
    observaciones: Optional[str]
    imagen_url: Optional[str]
    tipo_alimentacion: Optional[str]

class ResultadoTorqueCreate(ResultadoTorqueBase):
    pass

class ResultadoTorque(ResultadoTorqueBase):
    id: int
    test_id: int

    class Config:
        orm_mode = True

class TestTorqueBase(BaseModel):
    proyecto_id: int
    equipo_id: int
    usuario_id: Optional[int]

class TestTorqueCreate(TestTorqueBase):
    resultados: list[ResultadoTorqueCreate]

class TestTorque(TestTorqueBase):
    id: int
    fecha: datetime
    resultados: list[ResultadoTorque]

    class Config:
        orm_mode = True
