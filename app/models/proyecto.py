from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    
    # Rutas de logos
    logo_cliente = Column(String, nullable=True)
    logo_subcontrata = Column(String, nullable=True)

    # Relaciones con parámetros técnicos por tipo de prueba
    parametros_continuidad = relationship("ParametrosContinuidad", back_populates="proyecto")
    parametros_megado = relationship("ParametrosMegado", back_populates="proyecto")
    parametros_contact_resistance = relationship("ParametrosContactResistance", back_populates="proyecto")
    parametros_torque = relationship("ParametrosTorque", back_populates="proyecto")
