from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EquipmentCreate(BaseModel):
    project_id: int
    location_1_id: int
    number_location_1: int
    location_2_id: Optional[int] = None
    number_location_2: Optional[int] = None
    equipment_type_id: int
    number_equipment_type: int
    sub_equipment_id: Optional[int] = None
    number_sub_equipment: Optional[int] = None
    terminal: Optional[str] = None
    power_type: Optional[str] = None
    cable_set: Optional[int] = None


class EquipmentOut(BaseModel):
    id: int
    project_id: int
    location_1_id: int
    number_location_1: int
    location_2_id: Optional[int] = None
    number_location_2: Optional[int] = None
    equipment_type_id: int
    number_equipment_type: int
    sub_equipment_id: Optional[int] = None
    number_sub_equipment: Optional[int] = None
    terminal: Optional[str] = None
    power_type: Optional[str] = None
    cable_set: Optional[int] = None
    code: str
    creation_date: Optional[datetime]

    class Config:
        from_attributes = True
