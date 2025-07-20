# app/models/user_project.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UserProject(Base):
    __tablename__ = "user_project"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)

    user = relationship("User", back_populates="user_project")
    project = relationship("Project", back_populates="user_project")

