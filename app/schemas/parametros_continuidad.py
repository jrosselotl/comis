from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ParametrosContinuidadBase(BaseModel):
    cable_set: int
    punto: str
    logica: str           # Ej: "mayor_que", "menor_que", "igual"
    referencia: float
    unidad: str

class ParametrosContinuidadCreate(ParametrosContinuidadBase):
    proyecto_id: int

class ParametrosContinuidadUpdate(ParametrosContinuidadBase):
    pass

class ParametrosContinuidad(ParametrosContinuidadBase):
    id: int
    proyecto_id: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True
