from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    equipment = relationship("Equipment", back_populates="project")
    users_associated = relationship("UserProject", back_populates="project")

    client_logo = Column(String, nullable=True)
    subcontractor_logo = Column(String, nullable=True)

    # Tests
    test_continuity = relationship("TestContinuity", back_populates="project")
    test_isolation = relationship("TestIsolation", back_populates="project")
    test_contact_resistance = relationship("TestContactResistance", back_populates="project")
    test_torque = relationship("TestTorque", back_populates="project")
