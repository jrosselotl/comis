from sqlalchemy import Column, Integer, String, Enum, DateTime
from app.database import Base
import enum
from datetime import datetime

class RolUsuario(str, enum.Enum):
    admin = "admin"
    tecnico = "tecnico"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    rol = Column(String, default="tecnico")
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    tests_continuidad = relationship("TestContinuidad", back_populates="usuario")
    tests_megado = relationship("TestMegado", back_populates="usuario")


