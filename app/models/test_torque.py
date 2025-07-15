from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class TestTorque(Base):
    __tablename__ = "tests_torque"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    equipo_id = Column(Integer, ForeignKey("equipos.id"))
    tipo_alimentacion = Column(String, nullable=True)  # No siempre aplica en torque
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    resultados = relationship("ResultadoTorque", back_populates="test")
    proyecto = relationship("Proyecto", back_populates="tests_torque")
    equipo = relationship("Equipo", back_populates="tests_torque")
    usuario = relationship("Usuario", back_populates="tests_torque")


class ResultadoTorque(Base):
    __tablename__ = "resultados_torque"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests_torque.id"), nullable=False)
    cable_set = Column(Integer, nullable=False)
    punto_prueba = Column(String, nullable=False)
    valor_nominal = Column(String, nullable=False)
    valor_comprobacion = Column(String, nullable=True)
    resultado_valor = Column(String, nullable=True)
    unidad = Column(String, nullable=False)
    aprobado = Column(Boolean, default=False)
    observaciones = Column(String, nullable=True)
    imagen = Column(String, nullable=True)

    test = relationship("TestTorque", back_populates="resultados")
