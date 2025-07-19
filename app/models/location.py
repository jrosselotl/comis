from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from app.database import Base

class Ubicacion(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)

    ubicacion_1 = Column(String(50), nullable=False)
    numero_ubicacion_1 = Column(JSON, nullable=True)  # Ej: [1,2,3]
    ubicacion_2 = Column(String(50), nullable=True)
    numero_ubicacion_2 = Column(JSON, nullable=True)  # Ej: [1,2,3]
