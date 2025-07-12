from pydantic import BaseModel

class ParametrosContinuidadBase(BaseModel):
    proyecto_id: int
    codigo_equipo: str
    logica: str
    referencia: float
    unidad: str
    voltaje_requerido: float
    observaciones: str | None = None

class ParametrosContinuidadCreate(ParametrosContinuidadBase):
    pass

class ParametrosContinuidadOut(ParametrosContinuidadBase):
    id: int

    class Config:
        orm_mode = True
