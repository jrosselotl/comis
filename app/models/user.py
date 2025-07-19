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
    role = Column(String, default="technician")  # Can be admin, technician or project
    registration_date = Column(DateTime, default=datetime.utcnow)

    test_continuity = relationship("TestContinuity", back_populates="user")
    test_isolation = relationship("TestIsolation", back_populates="user")
    test_contact_resistance = relationship("TestContactResistance", back_populates="user")
    test_torque = relationship("TestTorque", back_populates="user")

    project_user = relationship("UserProject", back_populates="user")
