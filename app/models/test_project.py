from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TestProject(Base):
    __tablename__ = "test_project"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    test_id = Column(Integer, ForeignKey("test.id", ondelete="CASCADE"), nullable=False)
    active = Column(Boolean, default=True)

    # ✅ Relaciones correctas
    project = relationship("Project", back_populates="test_project")
    test = relationship("Test", back_populates="test_project")
