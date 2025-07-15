from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)

    # Clave foránea para vincular con Equipo
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)

    # Relación inversa
    equipo = relationship("Equipo", back_populates="tests")
