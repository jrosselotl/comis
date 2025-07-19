from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Proyecto(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)

    equipment = relationship("Equipo", back_populates="project")
    usuarios_asociados = relationship("UsuarioProyecto", back_populates="project")

    logo_cliente = Column(String, nullable=True)
    logo_subcontrata = Column(String, nullable=True)

    # Tests
    tests_continuidad = relationship("TestContinuidad", back_populates="project")
    tests_megado = relationship("TestMegado", back_populates="project")
    tests_contact_resistance = relationship("TestContactResistance", back_populates="project")
    tests_torque = relationship("TestTorque", back_populates="project")

