from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class RolUsuario(str, enum.Enum):
    admin = "admin"
    tecnico = "tecnico"
    proyecto = "proyecto"

class Usuario(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    rol = Column(String, default="tecnico")  # Puede ser admin, tecnico o proyecto
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    tests_continuidad = relationship("TestContinuidad", back_populates="user")
    tests_megado = relationship("TestMegado", back_populates="user")
    tests_contact_resistance = relationship("TestContactResistance", back_populates="user")
    tests_torque = relationship("TestTorque", back_populates="user")

    proyectos_asociados = relationship("UsuarioProyecto", back_populates="user")
