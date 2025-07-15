from pydantic import BaseModel
from typing import Optional

class ParametroMegadoBase(BaseModel):
    proyecto_id: int
    test_id: int
    codigo_equipo: str
    logica: str
    referencia: str
    unidad: str
    voltaje: Optional[str]
    duracion: Optional[str]

class ParametroMegadoCreate(ParametroMegadoBase):
    pass

class ParametroMegadoUpdate(BaseModel):
    proyecto_id: Optional[int]
    test_id: Optional[int]
    codigo_equipo: Optional[str]
    logica: Optional[str]
    referencia: Optional[str]
    unidad: Optional[str]
    voltaje: Optional[str]
    duracion: Optional[str]
