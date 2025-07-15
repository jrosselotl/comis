from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)

    # Relación con equipos
    equipos = relationship("Equipo", back_populates="proyecto")

    # Relación con usuarios asignados a proyectos
    usuarios_asociados = relationship("UsuarioProyecto", back_populates="proyecto")

    # Logos
    logo_cliente = Column(String, nullable=True)
    logo_subcontrata = Column(String, nullable=True)

    # ✅ Relaciones con tests (coinciden con los modelos de test)
    tests_continuidad = relationship("TestContinuidad", back_populates="proyecto")
    tests_megado = relationship("TestMegado", back_populates="proyecto")
    tests_contact_resistance = relationship("TestContactResistance", back_populates="proyecto")
    tests_torque = relationship("TestTorque", back_populates="proyecto")
