from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from app.database import Base

class TestTorque(Base):
    __tablename__ = "tests_torque"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    equipo_id = Column(Integer, ForeignKey("equipos.id"))
    tipo_alimentacion = Column(String, nullable=True)
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
    valor_nominal = Column(Float, nullable=False)  # se copia del parametro_torque
    valor_comprobacion = Column(Float, nullable=True)  # técnico lo ingresa
    unidad = Column(String, nullable=False)
    observaciones = Column(String, nullable=True)
    imagen = Column(String, nullable=True)

    test = relationship("TestTorque", back_populates="resultados")

