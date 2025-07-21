from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.equipment_type import EquipmentType

router = APIRouter(prefix="/equipment_type", tags=["Equipment Type"])

@router.get("/list")
def list_equipment_type(db: Session = Depends(get_db)):
    equipment_types = db.query(EquipmentType).all()
    return [
        {
            "equipment_type": t.equipment_type,
            "number_equipment_type": t.number_equipment_type if hasattr(t, "number_equipment_type") else [],
            "sub_equipment": t.sub_equipment if hasattr(t, "sub_equipment") else "",
            "number_sub_equipment": t.number_sub_equipment if hasattr(t, "number_sub_equipment") else []
        }
        for t in equipment_types
    ]
