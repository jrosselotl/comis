from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database import Base

class ParametrosTorque(Base):
    __tablename__ = "parametros_torque"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False)
    codigo_equipo = Column(String, nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    valor_nominal = Column(Float, nullable=False)
    valor_comprobacion = Column(Float, nullable=False)
    unidad = Column(String(50), nullable=False)
    observaciones = Column(String)
