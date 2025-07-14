from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ParametrosMegadoBase(BaseModel):
    cable_set: int
    punto: str
    logica: str           # Ej: "mayor_que", "menor_que", "igual"
    referencia: float
    unidad: str

class ParametrosMegadoCreate(ParametrosMegadoBase):
    proyecto_id: int

class ParametrosMegadoUpdate(ParametrosMegadoBase):
    pass

class ParametrosMegado(ParametrosMegadoBase):
    id: int
    proyecto_id: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True
