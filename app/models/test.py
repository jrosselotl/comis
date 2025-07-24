from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True)
    test_type = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
