from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class TipoEquipo(str, Enum):
    COLO = "COLO"
    CE = "CE"
    PDU = "PDU"
    BSW = "BSW"

# Para crear un nuevo equipo
class EquipoCreate(BaseModel):
    proyecto_id: int
    codigo_equipo: str
    tipo: TipoEquipo
    descripcion: Optional[str] = None

# Para mostrar un equipo
class EquipoOut(BaseModel):
    id: int
    proyecto_id: int
    codigo_equipo: str
    tipo: TipoEquipo
    descripcion: Optional[str]
    fecha_creacion: Optional[datetime]

class Config:
    from_attributes = True

