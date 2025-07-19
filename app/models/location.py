from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from app.database import Base


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)

    location_1 = Column(String(50), nullable=False)
    location_1_number = Column(JSON, nullable=True)  # Example: [1,2,3]
    location_2 = Column(String(50), nullable=True)
    location_2_number = Column(JSON, nullable=True)  # Example: [1,2,3]
