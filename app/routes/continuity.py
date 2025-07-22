from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

from app.models.test_continuity import TestContinuity, ResultContinuity
from app.models.test import Test
from app.models.equipment import Equipment
from app.models.test_performed import TestPerformed

import os, shutil, json
from datetime import datetime

router = APIRouter(prefix="/form/continuity", tags=["Continuity Form"])
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/save")
async def save_continuity_test(
    project_id: int = Form(...),
    location_1: str = Form(...),
    number_location_1: int = Form(...),
    location_2: str = Form(None),
    number_location_2: int = Form(None),
    equipment_type: str = Form(...),
    number_equipment_type: int = Form(...),
    sub_equipment: str = Form(None),
    number_sub_equipment: int = Form(None),
    test_type: str = Form(...),
    cable_set: int = Form(...),
    power_type: str = Form(...),
    terminal: str = Form(None),
    data: str = Form(...),
    images: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        data_parsed = json.loads(data)
        user_id = 1  # ✅ Temporal

        # ✅ 1) Verificar o crear equipo
        equipment_code = f"{location_1}-{equipment_type}-{number_equipment_type}".upper()
        equipment = db.query(Equipment).filter_by(code=equipment_code).first()
        if not equipment:
            equipment = Equipment(
                project_id=project_id,
                location_1=location_1,
                number_location_1=number_location_1,
                location_2=location_2,
                number_location_2=number_location_2,
                equipment_type=equipment_type,
                number_equipment_type=number_equipment_type,
                sub_equipment=sub_equipment,
                number_sub_equipment=number_sub_equipment,
                terminal=terminal,
                power_type=power_type,
                cable_set=cable_set,
                code=equipment_code
            )
            db.add(equipment)
            db.commit()
            db.refresh(equipment)

        # ✅ 2) Buscar ID del test en la tabla fija `test`
        test_fixed = db.query(Test).filter(Test.name == test_type).first()
        if not test_fixed:
            raise HTTPException(status_code=400, detail="Test type not found in fixed table")

        # ✅ 3) Insertar en test_performed
        test_performed = TestPerformed(
            project_id=project_id,
            equipment_id=equipment.id,
            user_id=user_id,
            test_id=test_fixed.id,
            status="Incomplete"
        )
        db.add(test_performed)
        db.commit()
        db.refresh(test_performed)

        # ✅ 4) Crear el test específico (test_continuity)
        continuity_test = TestContinuity(
            equipment_id=equipment.id,
            user_id=user_id,
            project_id=project_id,
            test_id=test_fixed.id
        )
        db.add(continuity_test)
        db.commit()
        db.refresh(continuity_test)

        # ✅ 5) Guardar resultados
        images_info = []
        for i, r in enumerate(data_parsed):
            image = images[i] if i < len(images) else None
            filename = f"{equipment_code}_{r['test_point']}_{i}.png" if image else None
            filepath = None

            if image:
                filepath = os.path.join(UPLOAD_DIR, filename)
                with open(filepath, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                images_info.append({
                    "path": filepath,
                    "test_point": r["test_point"],
                    "cable_set": r.get("cable_set")
                })

            result = ResultContinuity(
                test_id=continuity_test.id,
                test_point=r['test_point'],
                result_value=None if r['result_value'] == "N/A" else float(r['result_value']),
                unit=r.get('unit'),
                observation=r.get('observation'),
                image_url=filepath,
                cable_set=r.get("cable_set")
            )
            db.add(result)
        db.commit()

        return {"message": "Continuity test saved successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving continuity test: {str(e)}")
