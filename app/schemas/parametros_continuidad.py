from pydantic import BaseModel
from typing import Optional

class ParametroContinuidadBase(BaseModel):
    proyecto_id: int
    tipo_equipo: str
    logica: str
    referencia: float
    unidad: str

class ParametroContinuidadCreate(ParametroContinuidadBase):
    pass

class ParametroContinuidadUpdate(BaseModel):
    tipo_equipo: Optional[str]
    logica: Optional[str]
    referencia: Optional[float]
    unidad: Optional[str]
