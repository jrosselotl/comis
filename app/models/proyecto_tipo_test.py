from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class ProyectoTipoTest(Base):
    __tablename__ = "proyecto_tipo_test"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id", ondelete="CASCADE"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("proyecto_id", "test_id", name="uix_proyecto_test"),
    )

    # ✅ Relaciones necesarias
    proyecto = relationship("Proyecto", back_populates="tipo_test")
    test = relationship("Test")  # (opcional si quieres acceder a test.nombre directamente)
