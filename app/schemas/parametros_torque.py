from pydantic import BaseModel
from typing import Optional

class ParametroTorqueBase(BaseModel):
    proyecto_id: int
    test_id: int
    codigo_equipo: str
    valor_nominal: str
    valor_comprobacion: str
    unidad: str

class ParametroTorqueCreate(ParametroTorqueBase):
    pass

class ParametroTorqueUpdate(BaseModel):
    proyecto_id: Optional[int]
    test_id: Optional[int]
    codigo_equipo: Optional[str]
    valor_nominal: Optional[str]
    valor_comprobacion: Optional[str]
    unidad: Optional[str]
