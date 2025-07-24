from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    technician = "technician"
    project = "project"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="technician")  # admin, technician, or project
    registration_date = Column(DateTime, default=datetime.utcnow)

    # ✅ Relaciones correctas
    test_performed = relationship("TestPerformed", back_populates="user")
     user_project = relationship("UserProject", back_populates="user", cascade="all, delete-orphan")
