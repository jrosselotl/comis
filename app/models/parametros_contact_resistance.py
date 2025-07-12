from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database import Base

class ParametrosContactResistance(Base):
    __tablename__ = "parametros_contact_resistance"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False)
    codigo_equipo = Column(String, nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    logica = Column(String(10), nullable=False)  # Ej: =, <, <=, >, >=
    referencia = Column(Float, nullable=False)
    unidad = Column(String(50), nullable=False)
    voltaje_requerido = Column(Float, nullable=False)
    observaciones = Column(String)
