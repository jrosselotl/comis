from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ParametroTorque(Base):
    __tablename__ = "parametros_torque"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    cable_set = Column(Integer, nullable=False)
    punto_prueba = Column(String, nullable=False)
    valor_nominal = Column(Float, nullable=False)
    valor_comprobacion = Column(Float, nullable=True)  # el admin puede fijar tolerancia/referencia
    unidad = Column(String, nullable=False)

    proyecto = relationship("Proyecto", back_populates="parametros_torque")
