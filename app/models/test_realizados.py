from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TestRealizado(Base):
    __tablename__ = "test_realizados"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id", ondelete="CASCADE"))
    equipo_id = Column(Integer, ForeignKey("equipos.id", ondelete="CASCADE"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    test_id = Column(Integer, ForeignKey("tests.id", ondelete="CASCADE"))
    fecha = Column(DateTime, default=datetime.utcnow)
    estado = Column(String(50), default="Incompleto")

    proyecto = relationship("Proyecto")
    equipo = relationship("Equipo")
    usuario = relationship("Usuario")
