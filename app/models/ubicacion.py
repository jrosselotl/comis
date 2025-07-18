from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY
from app.database import Base

class Ubicacion(Base):
    __tablename__ = "ubicaciones"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False)
    ubicacion_1 = Column(String, nullable=False)
    numero_ubicacion_1 = Column(ARRAY(Integer), default=[])
    ubicacion_2 = Column(String, nullable=True)
    numero_ubicacion_2 = Column(ARRAY(Integer), default=[])
