from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)

    equipos = relationship("Equipo", back_populates="proyecto")
    usuarios_asociados = relationship("UsuarioProyecto", back_populates="proyecto")

    logo_cliente = Column(String, nullable=True)
    logo_subcontrata = Column(String, nullable=True)

    # Tests
    tests_continuidad = relationship("TestContinuidad", back_populates="proyecto")
    tests_megado = relationship("TestMegado", back_populates="proyecto")
    tests_contact_resistance = relationship("TestContactResistance", back_populates="proyecto")
    tests_torque = relationship("TestTorque", back_populates="proyecto")

    # Parámetros
    parametros_continuidad = relationship("ParametroContinuidad", back_populates="proyecto")
    parametros_megado = relationship("ParametroMegado", back_populates="proyecto")
    parametros_contact_resistance = relationship("ParametroContactResistance", back_populates="proyecto")
    parametros_torque = relationship("ParametroTorque", back_populates="proyecto")
