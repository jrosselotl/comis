from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True)
    test_type = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # ✅ Relaciones correctas
    test_project = relationship("TestProject", back_populates="test")
    test_performed = relationship("TestPerformed", back_populates="test")
