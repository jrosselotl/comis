from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    client_logo = Column(String, nullable=True)
    subcontractor_logo = Column(String, nullable=True)

    # ✅ Relaciones correctas
    equipment = relationship("Equipment", back_populates="project")
    user_project = relationship("UserProject", back_populates="project", cascade="all, delete-orphan")
    test_project = relationship("TestProject", back_populates="project")  # ✅ Tipos de tests asignados al proyecto
    test_performed = relationship("TestPerformed", back_populates="project", cascade="all, delete-orphan")  # ✅ Tests realizados
