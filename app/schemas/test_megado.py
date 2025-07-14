from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ResultadoMegadoBase(BaseModel):
    punto: str
    resultado_valor: Optional[float]
    unidad: str
    aprobado: str
    observaciones: Optional[str] = None
    imagen: Optional[str] = None

class ResultadoMegadoCreate(ResultadoMegadoBase):
    pass

class ResultadoMegado(ResultadoMegadoBase):
    id: int
    test_id: int

    class Config:
        orm_mode = True

class TestMegadoBase(BaseModel):
    equipo_id: int
    usuario_id: int
    test_id: int
    fecha: Optional[datetime] = None

class TestMegadoCreate(TestMegadoBase):
    resultados: List[ResultadoMegadoCreate]

class TestMegado(TestMegadoBase):
    id: int
    resultados: List[ResultadoMegado]

    class Config:
        orm_mode = True
