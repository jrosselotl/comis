from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)

    # Relación con Equipo
    equipos = relationship("Equipo", back_populates="proyecto")
    tipo_test = relationship("TipoTest", back_populates="proyecto")
    usuarios_asociados = relationship("UsuarioProyecto", back_populates="proyecto")
    
    # Rutas de logos
    logo_cliente = Column(String, nullable=True)
    logo_subcontrata = Column(String, nullable=True)

    # Relaciones con parámetros técnicos por tipo de prueba
    parametros_continuidad = relationship("ParametroContinuidad", back_populates="proyecto")
    parametros_megado = relationship("ParametroMegado", back_populates="proyecto")
    parametros_contact_resistance = relationship("ParametroContactResistance", back_populates="proyecto")
    parametros_torque = relationship("ParametroTorque", back_populates="proyecto")

