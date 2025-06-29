import enum
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from app.database import Base


class TipoEquipo(str, Enum):
    ADP = "ADP"
    ATS = "ATS"
    LBP = "LBP"
    MSB = "MSB"
    NLP = "NLP"
    PNL = "PNL"
    PDU = "PDU"


class SubEquipo(str, Enum):
    BSW = "BSW"
    FCB = "FCB"


class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False)

    ubicacion_1 = Column(String(50), nullable=True)
    ubicacion_2 = Column(String(50), nullable=True)
    tipo_equipo = Column("tipo_equipo", SQLEnum(TipoEquipo, name="tipo_equipo"), nullable=False)
    sub_equipo = Column(SQLEnum(SubEquipo, name="sub_equipo"), nullable=True)
    terminal = Column(String(50), nullable=True)
    tipo_alimentacion = Column(String(50), nullable=True)
    cable_set = Column(Integer, nullable=True)
    codigo = Column(String(100), unique=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    proyecto = relationship("Proyecto", back_populates="equipos")
    tests_continuidad = relationship("TestContinuidad", back_populates="equipo")
    tests_megado = relationship("TestMegado", back_populates="equipo")  


