from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.equipment import EquipmentCreate, EquipmentOut
from app.models.equipment import Equipment
from app.models.location import Location
from app.models.equipment_type import EquipmentType
from app.database import get_db

router = APIRouter(prefix="/equipment", tags=["Equipment"])


@router.post("/", response_model=EquipmentOut)
def create_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    # ✅ Build dynamic code using related table names
    location_1 = db.query(Location).filter_by(id=equipment.location_1_id).first()
    location_2 = db.query(Location).filter_by(id=equipment.location_2_id).first() if equipment.location_2_id else None
    equipment_type = db.query(EquipmentType).filter_by(id=equipment.equipment_type_id).first()
    sub_equipment = db.query(EquipmentType).filter_by(id=equipment.sub_equipment_id).first() if equipment.sub_equipment_id else None

    if not location_1 or not equipment_type:
        raise HTTPException(status_code=400, detail="Location or equipment type is not valid")

    code = f"{location_1.name}{equipment.number_location_1}"
    if location_2:
        code += f"-{location_2.name}{equipment.number_location_2 or ''}"
    code += f"-{equipment_type.name}{equipment.number_equipment_type}"
    if sub_equipment:
        code += f"-{sub_equipment.name}{equipment.number_sub_equipment or ''}"

    new_equipment = Equipment(
        project_id=equipment.project_id,
        location_1_id=equipment.location_1_id,
        number_location_1=equipment.number_location_1,
        location_2_id=equipment.location_2_id,
        number_location_2=equipment.number_location_2,
        equipment_type_id=equipment.equipment_type_id,
        number_equipment_type=equipment.number_equipment_type,
        sub_equipment_id=equipment.sub_equipment_id,
        number_sub_equipment=equipment.number_sub_equipment,
        terminal=equipment.terminal,
        power_type=equipment.power_type,
        cable_set=equipment.cable_set,
        code=code
    )

    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)
    return new_equipment


@router.get("/list", response_model=list[EquipmentOut])
def list_equipment(db: Session = Depends(get_db)):
    return db.query(Equipment).all()
