from sqlalchemy import Column, Integer, String, ARRAY
from app.database import Base

class TipoEquipo(Base):
    __tablename__ = "tipo_equipos"

    id = Column(Integer, primary_key=True, index=True)
    tipo_equipo = Column(String, nullable=False)
    numero_tipo_equipo = Column(ARRAY(Integer), default=[])
    sub_equipo = Column(String, nullable=True)
    numero_sub_equipo = Column(ARRAY(Integer), default=[])
