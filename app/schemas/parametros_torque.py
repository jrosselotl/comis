from pydantic import BaseModel

class ParametrosTorqueBase(BaseModel):
    proyecto_id: int
    codigo_equipo: str
    valor_nominal: float
    valor_comprobacion: float
    unidad: str
    observaciones: str | None = None

class ParametrosTorqueCreate(ParametrosTorqueBase):
    pass

class ParametrosTorqueOut(ParametrosTorqueBase):
    id: int

    class Config:
        orm_mode = True
