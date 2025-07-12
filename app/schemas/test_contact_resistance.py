from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ResultadoContactResistanceBase(BaseModel):
    cable_set: int
    punto_prueba: str
    referencia_valor: Optional[float]
    resultado_valor: Optional[float]
    aprobado: Optional[bool] = False
    observaciones: Optional[str] = None
    imagen_url: Optional[str] = None
    tipo_alimentacion: Optional[str] = None
    unidad: Optional[str] = None

class ResultadoContactResistanceCreate(ResultadoContactResistanceBase):
    pass

class ResultadoContactResistance(ResultadoContactResistanceBase):
    id: int
    test_id: int

    class Config:
        orm_mode = True

class TestContactResistanceBase(BaseModel):
    proyecto_id: int
    equipo_id: int
    usuario_id: Optional[int] = None
    fecha: Optional[datetime] = None

class TestContactResistanceCreate(TestContactResistanceBase):
    resultados: list[ResultadoContactResistanceCreate]

class TestContactResistance(TestContactResistanceBase):
    id: int
    resultados: list[ResultadoContactResistance]

    class Config:
        orm_mode = True
