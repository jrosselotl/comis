from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)

    # 🔹 Ahora Foreign Keys hacia las nuevas tablas dinámicas
    ubicacion_1_id = Column(Integer, ForeignKey("ubicaciones.id"), nullable=False)
    ubicacion_2_id = Column(Integer, ForeignKey("ubicaciones.id"), nullable=True)

    tipo_equipo_id = Column(Integer, ForeignKey("tipo_equipos.id"), nullable=False)
    sub_equipo_id = Column(Integer, ForeignKey("tipo_equipos.id"), nullable=True)

    numero_ubicacion_1 = Column(Integer, nullable=False, default=1)
    numero_ubicacion_2 = Column(Integer, nullable=True)
    numero_tipo_equipo = Column(Integer, nullable=False, default=1)
    numero_sub_equipo = Column(Integer, nullable=True)

    terminal = Column(String(50), nullable=True)
    tipo_alimentacion = Column(String(50), nullable=True)
    cable_set = Column(Integer, nullable=True)
    codigo = Column(String(100), unique=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="equipos")
    ubicacion_1 = relationship("Ubicacion", foreign_keys=[ubicacion_1_id])
    ubicacion_2 = relationship("Ubicacion", foreign_keys=[ubicacion_2_id])
    tipo_equipo = relationship("TipoEquipo", foreign_keys=[tipo_equipo_id])
    sub_equipo = relationship("TipoEquipo", foreign_keys=[sub_equipo_id])

    tests_continuidad = relationship("TestContinuidad", back_populates="equipo")
    tests_megado = relationship("TestMegado", back_populates="equipo")
    tests_contact_resistance = relationship("TestContactResistance", back_populates="equipo")
    tests_torque = relationship("TestTorque", back_populates="equipo")
