from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EquipoCreate(BaseModel):
    proyecto_id: int
    ubicacion_1_id: int
    numero_ubicacion_1: int
    ubicacion_2_id: Optional[int] = None
    numero_ubicacion_2: Optional[int] = None
    tipo_equipo_id: int
    numero_tipo_equipo: int
    sub_equipo_id: Optional[int] = None
    numero_sub_equipo: Optional[int] = None
    terminal: Optional[str] = None
    tipo_alimentacion: Optional[str] = None
    cable_set: Optional[int] = None


class EquipoOut(BaseModel):
    id: int
    proyecto_id: int
    ubicacion_1_id: int
    numero_ubicacion_1: int
    ubicacion_2_id: Optional[int] = None
    numero_ubicacion_2: Optional[int] = None
    tipo_equipo_id: int
    numero_tipo_equipo: int
    sub_equipo_id: Optional[int] = None
    numero_sub_equipo: Optional[int] = None
    terminal: Optional[str] = None
    tipo_alimentacion: Optional[str] = None
    cable_set: Optional[int] = None
    codigo: str
    fecha_creacion: Optional[datetime]

    class Config:
        from_attributes = True
