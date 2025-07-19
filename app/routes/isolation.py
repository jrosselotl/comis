from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_megado import TestMegado, ResultadoMegado
from app.models.test import Test
from app.models.equipment import Equipment
from app.models.project import Project
from app.utils.pdf_generator import generar_pdf_test
from app.utils.correo import enviar_correo_con_pdf, obtener_correos_admins

import os, shutil, json
from datetime import datetime

router = APIRouter(prefix="/formulario/megado", tags=["Form Megado"])
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/guardar")
async def save_test_megado(
    project_id: int = Form(...),
    location_1: str = Form(...),
    number_location_1: str = Form(...),
    location_2: str = Form(None),
    number_location_2: str = Form(None),
    equipment_type: str = Form(...),
    number_equipment_type: str = Form(...),
    sub_equipment: str = Form(None),
    number_sub_equipment: str = Form(None),
    test_type: str = Form(...),
    cable_sets: int = Form(...),
    power_type: str = Form(...),
    terminal: str = Form(None),
    data: str = Form(...),
    images: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    data_parsed = json.loads(data)
    user_id = 1  # 🔹 Será dinámico con autenticación en el futuro

    # ✅ Generate unique equipment code
    equipment_code = f"{location_1}-{equipment_type}-{sub_equipment or 'GEN'}{number_sub_equipment or ''}".upper()

    # ✅ Check or create equipment
    equipment = db.query(Equipment).filter_by(codigo=equipment_code).first()
    if not equipment:
        equipment = Equipment(
            codigo=equipment_code,
            tipo=equipment_type,
            sub_equipo=sub_equipment,
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

    # ✅ Create specific Megado test
    test_meg = TestMegado(
        equipment_id=equipment.id,
        user_id=user_id,
        test_id=test.id
    )
    db.add(test_meg)
    db.commit()
    db.refresh(test_meg)

    # ✅ Save results (without parameters or approval logic)
    images_info = []
    pdf_results = []

    for i, r in enumerate(data_parsed):
        image = images[i] if i < len(images) else None
        filename = f"{equipment_code}_{r['punto_prueba']}_{i}.png" if image else None
        filepath = None

        if image:
            filepath = os.path.join(UPLOAD_DIR, filename)
            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            images_info.append({
                "path": filepath,
                "punto_prueba": r["punto_prueba"],
                "cable_set": r.get("cable_set")
            })

        result = ResultadoMegado(
            test_id=test_meg.id,
            punto=r['punto_prueba'],
            resultado_valor=None if r['resultado_valor'] == "N/A" else float(r['resultado_valor']),
            unidad=r['unidad'],
            tiempo_aplicado=float(r.get('tiempo_aplicado', 0)),  # Technician inputs manually
            observaciones=r.get('observaciones'),
            imagen=filepath,
            cable_set=r.get("cable_set")
        )
        db.add(result)

        pdf_results.append({
            "punto_prueba": r["punto_prueba"],
            "resultado_valor": r["resultado_valor"],
            "unidad": r["unidad"],
            "tiempo_aplicado": r.get('tiempo_aplicado', 0),
            "observaciones": r.get("observaciones", ""),
            "cable_set": r.get("cable_set")
        })

    db.commit()

    # ✅ Data for PDF
    project = db.query(Project).filter_by(id=project_id).first()
    equipment_details = {
        "Project": project.nombre,
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
        "detalles_equipo": equipment_details,
        "imagenes": images_info,
        "logo_cliente": f"logo_cliente_{project.nombre}.png",
        "logo_subcontrata": f"logo_subcontrata_{project.nombre}.png",
        "user_name": "Technician"
    }

    # ✅ Generate PDF
    output_pdf_path = f"output/{test_type}_{equipment_code}.pdf"
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    generar_pdf_test(test_data, pdf_results, output_path=output_pdf_path)

    # ✅ Send email
    emails = obtener_correos_admins(db, project_id)
    enviar_correo_con_pdf(
        destinatarios=emails,
        asunto=f"{test_type.capitalize()} - {equipment_code}",
        cuerpo=f"Report of {test_type} for equipment {equipment_code}",
        archivo_pdf=output_pdf_path
    )

    return {"message": "Form and results saved successfully"}
