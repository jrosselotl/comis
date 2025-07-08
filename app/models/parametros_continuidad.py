from sqlalchemy import Column, Integer, Float, String
from app.database import Base

class ParametrosContinuidad(Base):
    __tablename__ = "parametros_continuidad"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, nullable=False)
    codigo_equipo = Column(String, nullable=False)
    valor_minimo = Column(Float, nullable=False)
    valor_maximo = Column(Float, nullable=False)
    unidad = Column(String, nullable=False)
    voltaje_requerido = Column(Float, nullable=False)
    observaciones = Column(String)
