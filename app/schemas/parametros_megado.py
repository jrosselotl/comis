from pydantic import BaseModel

class ParametrosMegadoBase(BaseModel):
    proyecto_id: int
    codigo_equipo: str
    logica: str
    referencia: float
    unidad: str
    voltaje_requerido: float
    observaciones: str | None = None

class ParametrosMegadoCreate(ParametrosMegadoBase):
    pass

class ParametrosMegadoOut(ParametrosMegadoBase):
    id: int

    class Config:
        orm_mode = True
