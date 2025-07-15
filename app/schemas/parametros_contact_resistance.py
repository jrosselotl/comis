from pydantic import BaseModel
from typing import Optional

class ParametroContactResistanceBase(BaseModel):
    proyecto_id: int
    test_id: int
    codigo_equipo: str
    logica: str
    referencia: str
    unidad: str

class ParametroContactResistanceCreate(ParametroContactResistanceBase):
    pass

class ParametroContactResistanceUpdate(BaseModel):
    proyecto_id: Optional[int]
    test_id: Optional[int]
    codigo_equipo: Optional[str]
    logica: Optional[str]
    referencia: Optional[str]
    unidad: Optional[str]
