# app/models/usuarios_proyectos.py

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UsuarioProyecto(Base):
    __tablename__ = "usuarios_proyectos"

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), primary_key=True)

    usuario = relationship("Usuario", back_populates="proyectos_asociados")
    proyecto = relationship("Proyecto", back_populates="usuarios_asociados")
