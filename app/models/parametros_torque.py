from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ParametroTorque(Base):
    __tablename__ = "parametros_torque"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    valor_nominal = Column(String, nullable=False)
    valor_comprobacion = Column(String, nullable=False)
    unidad = Column(String, nullable=False)  # Ej: 'Nm'

    proyecto = relationship("Proyecto", back_populates="parametros_torque")
