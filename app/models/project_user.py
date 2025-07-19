from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UserProject(Base):
    __tablename__ = "user_project"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"), primary_key=True)

    user = relationship("User", back_populates="project_user")
    project = relationship("Project", back_populates="user_project")
