from pydantic import BaseModel, validator
from typing import Optional
from enum import Enum
from datetime import datetime

class TipoEquipo(str, Enum):
    ADP = "ADP"
    ATS = "ATS"
    LBP = "LBP"
    MSB = "MSB"
    NLP = "NLP"
    PNL = "PNL"
    PDU = "PDU"

class SubEquipo(str, Enum):
    BSW = "BSW"
    FCB = "FCB"

class EquipoCreate(BaseModel):
    proyecto_id: int
    ubicacion_1: Optional[str]
    ubicacion_2: Optional[str]
    tipo: TipoEquipo
    numero_tipo_equipo: Optional[int]
    sub_equipo: Optional[SubEquipo]
    terminal: Optional[str]
    tipo_alimentacion: Optional[str]
    cable_set: Optional[int]

    @validator("ubicacion_1")
    def validar_ubicacion_1(cls, v, values):
        if values.get("proyecto_id") == 1:
            if v not in ["COLO", "WTP", "ADMIN"]:
                raise ValueError("Ubicación 1 inválida para MAD03")
        return v

    @validator("ubicacion_2")
    def validar_ubicacion_2(cls, v, values):
        if values.get("proyecto_id") == 1 and v != "CE":
            raise ValueError("Ubicación 2 debe ser 'CE' en MAD03")
        return v

    @validator("sub_equipo")
    def validar_sub_equipo(cls, v, values):
        if values.get("tipo") in ["MSB", "PDU"] and v not in [None, "BSW", "FCB"]:
            raise ValueError("Sub-equipo inválido para este tipo")
        return v

class EquipoOut(BaseModel):
    id: int
    proyecto_id: int
    ubicacion_1: Optional[str]
    ubicacion_2: Optional[str]
    tipo: TipoEquipo
    numero_tipo_equipo: Optional[int]
    sub_equipo: Optional[SubEquipo]
    terminal: Optional[str]
    tipo_alimentacion: Optional[str]
    cable_set: Optional[int]
    fecha_creacion: Optional[datetime]

    class Config:
        from_attributes = True
