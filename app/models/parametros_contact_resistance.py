from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ParametroContactResistance(Base):
    __tablename__ = "parametros_contact_resistance"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    logica = Column(String, nullable=False)
    referencia = Column(String, nullable=False)

    proyecto = relationship("Proyecto", back_populates="parametros_contact_resistance")
