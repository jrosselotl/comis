from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_isolation import TestIsolation, ResultIsolation
from app.models.test import Test
from app.models.equipment import Equipment
from app.models.project import Project
from app.utils.pdf_generator import generate_test_pdf
from app.utils.email import send_email_with_pdf, get_admin_emails

import os
import shutil
import json
from datetime import datetime

router = APIRouter(prefix="/form/isolation", tags=["Form Isolation"])
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/save")
async def save_test_isolation(
    project_id: int = Form(...),
    location_1: str = Form(...),
    location_number_1: str = Form(...),
    location_2: str = Form(None),
    location_number_2: str = Form(None),
    equipment_type: str = Form(...),
    equipment_type_number: str = Form(...),
    sub_equipment: str = Form(None),
    sub_equipment_number: str = Form(None),
    test_type: str = Form(...),
    cable_set: int = Form(...),
    power_type: str = Form(...),
    terminal: str = Form(None),
    data: str = Form(...),
    images: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    data_parsed = json.loads(data)
    user_id = 1  # ✅ Will be dynamic in the future

    # ✅ Generate unique equipment code
    equipment_code = f"{location_1}-{equipment_type}-{sub_equipment or 'GEN'}{sub_equipment_number or ''}".upper()

    # ✅ Check or create equipment
    equipment = db.query(Equipment).filter_by(code=equipment_code).first()
    if not equipment:
        equipment = Equipment(
            code=equipment_code,
            equipment_type=equipment_type,
            sub_equipment=sub_equipment,
            project_id=project_id
        )
        db.add(equipment)
        db.commit()
        db.refresh(equipment)

    # ✅ Create general test record
    test = Test(test_type=test_type, equipment_id=equipment.id)
    db.add(test)
    db.commit()
    db.refresh(test)

    # ✅ Create specific Isolation test
    test_iso = TestIsolation(
        equipment_id=equipment.id,
        user_id=user_id,
        test_id=test.id
    )
    db.add(test_iso)
    db.commit()
    db.refresh(test_iso)

    # ✅ Save results (no parameters or validation logic)
    images_info = []
    pdf_results = []

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

        result = ResultIsolation(
            test_id=test_iso.id,
            test_point=r["test_point"],
            result_value=None if r["result_value"] == "N/A" else float(r["result_value"]),
            unit=r["unit"],
            applied_time=float(r.get("applied_time", 0)),
            observation=r.get("observation"),
            image=filepath,
            cable_set=r.get("cable_set")
        )
        db.add(result)

        pdf_results.append({
            "test_point": r["test_point"],
            "result_value": r["result_value"],
            "unit": r["unit"],
            "applied_time": r.get("applied_time", 0),
            "observation": r.get("observation", ""),
            "cable_set": r.get("cable_set")
        })

    db.commit()

    # ✅ Data for PDF
    project = db.query(Project).filter_by(id=project_id).first()
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
        "client_logo": f"logo_client_{project.name}.png",
        "subcontractor_logo": f"logo_subcontractor_{project.name}.png",
        "user_name": "Technician"
    }

    # ✅ Generate PDF
    output_pdf_path = f"output/{test_type}_{equipment_code}.pdf"
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    generate_test_pdf(test_data, pdf_results, output_path=output_pdf_path)

    # ✅ Send email
    emails = get_admin_emails(db, project_id)
    send_email_with_pdf(
        recipients=emails,
        subject=f"{test_type.capitalize()} - {equipment_code}",
        body=f"Isolation test report for equipment {equipment_code}",
        pdf_file=output_pdf_path
    )

    return {"message": "Form and results saved successfully"}
