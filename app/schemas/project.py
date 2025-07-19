from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Create project
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

# Read project
class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    creation_date: Optional[datetime]

    class Config:
        from_attributes = True
