from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.project import Project
from app.models.test import Test
from app.models.equipment import Equipment
from app.models.test_performed import TestPerformed
from app.models.result_continuity import ResultContinuity
from app.models.result_isolation import ResultIsolation
from app.models.result_contact_resistance import ResultContactResistance
from app.models.result_torque import ResultTorque
from app.routes.auth import get_current_user
from app.models.user import User
from app.utils.pdf_generator import generate_test_pdf
from app.utils.email import send_email_with_pdf, get_admin_emails

import os
import shutil
from datetime import datetime
import json

router = APIRouter(prefix="/form", tags=["Form"])
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/save")
async def save_form(
    request: Request,
    project_id: int = Form(...),
    location_1: str = Form(...),
    number_location_1: int = Form(...),
    location_2: Optional[str] = Form(None),
    number_location_2: Optional[int] = Form(None),
    equipment_type: str = Form(...),
    number_equipment_type: Optional[int] = Form(None),
    sub_equipment: Optional[str] = Form(None),
    number_sub_equipment: Optional[int] = Form(None),
    test_type: str = Form(...),
    cable_set: int = Form(...),
    power_type: str = Form(...),
    terminal: Optional[str] = Form(None),
    unit: Optional[str] = Form(None),
    data: str = Form(...),
    images: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    user_id = current_user.id
    print(f"✅ Usuario autenticado que guarda la prueba: {user_id}")

    # --- NORMALIZAMOS CAMPOS VACÍOS ---
    location_2 = location_2 or None
    number_location_2 = number_location_2 or None
    sub_equipment = sub_equipment or None
    number_sub_equipment = number_sub_equipment or None

    # --- EQUIPMENT (crea si no existe) ---
    equipment_code_parts = [f"{location_1}{number_location_1}"]
    if location_2 and number_location_2:
        equipment_code_parts.append(f"{location_2}{number_location_2}")
    equipment_code_parts.append(f"{equipment_type}{number_equipment_type}")
    if sub_equipment and number_sub_equipment:
        equipment_code_parts.append(f"{sub_equipment}{number_sub_equipment}")
    equipment_code = "-".join(equipment_code_parts).upper()

    equipment = db.query(Equipment).filter(Equipment.code == equipment_code).first()
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

    # --- TEST_PERFORMED ---
    test_fixed = db.query(Test).filter(Test.test_type == test_type).first()
    if not test_fixed:
        raise HTTPException(status_code=400, detail=f"Test '{test_type}' not found")

    new_test_performed = TestPerformed(
        project_id=project_id,
        equipment_id=equipment.id,
        user_id=user_id,
        test_id=test_fixed.id,
        status="completed"  # ✅ Puedes dejarlo "completed" directo si ya se completó
    )
    db.add(new_test_performed)
    db.commit()
    db.refresh(new_test_performed)

    # --- PARSEAMOS DATA ---
    try:
        data_parsed = json.loads(data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid data format")

    img_iter = iter(images)
    images_info = []

    # --- GUARDADO DE RESULTADOS ---
    MODEL_MAP = {
        "continuity": ResultContinuity,
        "isolation": ResultIsolation,
        "contact_resistance": ResultContactResistance,
        "torque": ResultTorque
    }
    ResultModel = MODEL_MAP.get(test_type)
    if not ResultModel:
        raise HTTPException(status_code=400, detail="Invalid test type")

    for r in data_parsed:
        image = next(img_iter, None)
        path = None
        if image and image.filename:
            filename = f"{datetime.utcnow().timestamp()}_{image.filename}"
            path = os.path.join(UPLOAD_DIR, filename)
            with open(path, "wb") as f:
                shutil.copyfileobj(image.file, f)
            images_info.append({
                "cable_set": r.get("cable_set"),
                "test_point": r["test_point"],
                "path": path
            })

        db.add(ResultModel(
            test_performed_id=new_test_performed.id,
            test_point=r["test_point"],
            result_value=None if r.get("result_value") == "N/A" else r.get("result_value"),
            unit=r.get("unit") or unit,
            observation=r.get("observation", ""),
            image_url=path,
            cable_set=r.get("cable_set"),
            time_applied=r.get("applied_time"),           # isolation
            nominal_value=r.get("nominal_value"),         # torque
            verification_value=r.get("verification_value")# torque
        ))

    db.commit()

    # --- GENERACIÓN PDF ---
    project = db.query(Project).filter(Project.id == project_id).first()
    equipment_details = {
        "Project": project.name,
        "Main Location": f"{location_1} Nº{number_location_1}",
        "Secondary Location": f"{location_2} Nº{number_location_2}" if location_2 else "-",
        "Equipment Type": f"{equipment_type} Nº{number_equipment_type}",
        "Sub Equipment": f"{sub_equipment} Nº{number_sub_equipment}" if sub_equipment else "-",
        "Power Type": power_type,
        "Terminal": terminal
    }
    test_data = {
        "equipment_id": equipment_code,
        "test_type": test_type,
        "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "equipment_details": equipment_details,
        "images": images_info,
        "user_name": current_user.name,
        "client_logo": project.client_logo,
        "subcontractor_logo": project.subcontractor_logo
    }
    pdf_results = [
        {
            "test_point": r["test_point"],
            "result_value": r.get("result_value"),
            "unit": r.get("unit") or unit,
            "observation": r.get("observation", ""),
            "cable_set": r.get("cable_set"),
            "nominal_value": r.get("nominal_value"),
            "verification_value": r.get("verification_value")
        }
        for r in data_parsed
    ]

    output_pdf_path = f"output/{test_type}_{equipment_code}.pdf"
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    generate_test_pdf(test_data, pdf_results, output_path=output_pdf_path)

    # --- EMAIL ---
    emails = get_admin_emails(db, project_id)
    send_email_with_pdf(
        recipients=emails,
        subject=f"{test_type.capitalize()} - {equipment_code}",
        body=f"Test report: {test_type} for equipment {equipment_code}",
        pdf_file=output_pdf_path
    )

    return {"message": "Form and results saved successfully"}
