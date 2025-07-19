from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TestRealizado(Base):
    __tablename__ = "test_realizados"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id", ondelete="CASCADE"))
    equipment_id = Column(Integer, ForeignKey("equipment.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    test_id = Column(Integer, ForeignKey("test.id", ondelete="CASCADE"))
    date = Column(DateTime, default=datetime.utcnow)
    estado = Column(String(50), default="Incompleto")

    projet = relationship("Project")
    equipment = relationship("Equipment")
    user = relationship("User")
