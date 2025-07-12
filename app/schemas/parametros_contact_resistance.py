from pydantic import BaseModel

class ParametrosContactResistanceBase(BaseModel):
    proyecto_id: int
    codigo_equipo: str
    logica: str
    referencia: float
    unidad: str
    voltaje_requerido: float
    observaciones: str | None = None

class ParametrosContactResistanceCreate(ParametrosContactResistanceBase):
    pass

class ParametrosContactResistanceOut(ParametrosContactResistanceBase):
    id: int

    class Config:
        orm_mode = True
