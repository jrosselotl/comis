from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.database import Base

class ProyectoTipoTest(Base):
    __tablename__ = "proyecto_tipo_test"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id", ondelete="CASCADE"), nullable=False)
    tipo_test = Column(Integer, nullable=False)  # 1 = continuidad, 2 = megado, 3 = torque, etc.

    __table_args__ = (
        UniqueConstraint('proyecto_id', 'tipo_test', name='uix_proyecto_tipo_test'),
    )
