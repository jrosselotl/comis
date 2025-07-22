from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Optional

# Test models
from app.models.test_continuity import TestContinuity, ResultContinuity
from app.models.test_isolation import TestIsolation, ResultIsolation
from app.models.test_contact_resistance import TestContactResistance, ResultContactResistance
from app.models.test_torque import TestTorque, ResultTorque

# Other models
from app.models.project import Project
from app.models.test import Test
from app.models.equipment import Equipment
from app.models.test_performed import TestPerformed  # ✅ Dashboard / My Tests

# Utilities
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
    project_id: Optional[str] = Form(None),
    location_1: Optional[str] = Form(None),
    number_location_1: Optional[str] = Form(None),
    location_2: Optional[str] = Form(None),
    number_location_2: Optional[str] = Form(None),
    equipment_type: Optional[str] = Form(None),
    number_equipment_type: Optional[str] = Form(None),
    sub_equipment: Optional[str] = Form(None),
    number_sub_equipment: Optional[str] = Form(None),
    test_type: Optional[str] = Form(None),
    cable_set: Optional[str] = Form(None),
    power_type: Optional[str] = Form(None),
    terminal: Optional[str] = Form(None),
    unit: Optional[str] = Form(None),
    data: Optional[str] = Form(None),
    images: Optional[list[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    print("📥 RAW FORM DATA:")
    print({
        "project_id": project_id,
        "number_location_1": number_location_1,
        "number_location_2": number_location_2,
        "number_equipment_type": number_equipment_type,
        "number_sub_equipment": number_sub_equipment,
        "cable_set": cable_set
    })


    # ✅ Si llegan strings vacíos, los convertimos a None
    if location_2 == "":
        location_2 = None
    if number_location_2 in ["", 0]:
        number_location_2 = None
    if sub_equipment == "":
        sub_equipment = None
    if number_sub_equipment in ["", 0]:
        number_sub_equipment = None
    
    # ✅ --- EQUIPMENT (con código completo) ---
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
    
    # ✅ --- TEST GENERAL (tabla fija) ---
    test_fixed = db.query(Test).filter(Test.name == test_type).first()
    if not test_fixed:
        raise HTTPException(status_code=400, detail=f"Test '{test_type}' not found in fixed table")

    # ✅ --- REGISTER IN TEST_PERFORMED ---
    new_test_performed = TestPerformed(
        project_id=project_id,
        equipment_id=equipment.id,
        user_id=user_id,
        test_id=test_general.id,
        status="Incomplete"
    )
    db.add(new_test_performed)
    db.commit()

    # --- IMAGES ---
    images_info = []
    img_iter = iter(images)

    # --- GENERIC FUNCTION TO SAVE RESULTS ---
    def save_results(test_model, result_model):
        test_instance = test_model(equipment_id=equipment.id, test_id=test_general.id, user_id=user_id)
        db.add(test_instance)
        db.commit()
        db.refresh(test_instance)

        for r in data_parsed:
            image = next(img_iter, None)
            filename = f"{datetime.utcnow().timestamp()}_{image.filename}" if image else None
            path = None
            if image:
                path = os.path.join(UPLOAD_DIR, filename)
                with open(path, "wb") as f:
                    shutil.copyfileobj(image.file, f)
                images_info.append({
                    "cable_set": r.get("cable_set"),
                    "test_point": r["test_point"],
                    "path": path
                })

            result = result_model(
                test_id=test_instance.id,
                test_point=r["test_point"],
                result_value=None if r["result_value"] == "N/A" else float(r["result_value"]),
                unit=r.get("unit") or unit,  # ✅ Usa la global si no viene por fila
                observation=r.get("observation", ""),
                image=path,
                cable_set=r.get("cable_set"),
                applied_time=float(r.get("applied_time", 0)) if "applied_time" in r else None,
                nominal_value=float(r.get("nominal_value", 0)) if "nominal_value" in r else None,
                check_value=float(r.get("check_value", 0)) if "check_value" in r else None
            )
            db.add(result)
        db.commit()

    # --- TEST SELECTION ---
    if test_type == "continuity":
        save_results(TestContinuity, ResultContinuity)
    elif test_type == "isolation":
        save_results(TestIsolation, ResultIsolation)
    elif test_type == "contact_resistance":
        save_results(TestContactResistance, ResultContactResistance)
    elif test_type == "torque":
        save_results(TestTorque, ResultTorque)
    else:
        raise HTTPException(status_code=400, detail="Test type not recognized")

    # --- PDF DATA ---
    project = db.query(Project).filter(Project.id == project_id).first()
    equipment_details = {
        "Project": project.name,
        "Main Location": f"{location_1} Nº{location_number_1}",
        "Secondary Location": f"{location_2} Nº{location_number_2}" if location_2 else "-",
        "Equipment Type": f"{equipment_type} Nº{equipment_type_number}",
        "Sub Equipment": f"{sub_equipment} Nº{sub_equipment_number}" if sub_equipment else "-",
        "Power Type": power_type,
        "Terminal": terminal
    }
    test_data = {
        "equipment_id": equipment_code,
        "test_type": test_type,
        "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "equipment_details": equipment_details,
        "images": images_info,
        "user_name": "Technician",
        "client_logo": f"logo_client_{project.name}.png",
        "subcontractor_logo": f"logo_subcontractor_{project.name}.png"
    }
    pdf_results = [
        {
            "test_point": r["test_point"],
            "result_value": r["result_value"],
            "unit": r.get("unit") or unit,  # ✅ También aquí, para PDF
            "observation": r.get("observation", ""),
            "cable_set": r.get("cable_set"),
            "nominal_value": r.get("nominal_value"),
            "check_value": r.get("check_value")
        }
        for r in data_parsed
    ]

    # --- GENERATE PDF ---
    output_pdf_path = f"output/{test_type}_{equipment_code}.pdf"
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    generate_test_pdf(test_data, pdf_results, output_path=output_pdf_path)

    # --- SEND EMAIL ---
    emails = get_admin_emails(db, project_id)
    send_email_with_pdf(
        recipients=emails,
        subject=f"{test_type.capitalize()} - {equipment_code}",
        body=f"Test report: {test_type} for equipment {equipment_code}",
        pdf_file=output_pdf_path
    )

    return {"message": "Form and results saved successfully"}
