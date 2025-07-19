# app/models/usuarios_proyectos.py

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UsuarioProyecto(Base):
    __tablename__ = "usuarios_proyectos"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"), primary_key=True)

    user = relationship("User", back_populates="proyectos_asociados")
    project = relationship("Project", back_populates="usuarios_asociados")
