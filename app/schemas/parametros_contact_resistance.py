from pydantic import BaseModel
from typing import Optional

class ParametroContactResistanceBase(BaseModel):
    logica: str
    referencia: str
    unidad: str
    proyecto_id: int

class ParametroContactResistanceCreate(ParametroContactResistanceBase):
    pass

class ParametroContactResistanceUpdate(BaseModel):
    logica: Optional[str]
    referencia: Optional[str]
    unidad: Optional[str]
