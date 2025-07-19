from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

# Modelos de pruebas
from app.models.test_continuidad import TestContinuidad, ResultadoContinuidad
from app.models.test_megado import TestMegado, ResultadoMegado
from app.models.test_contact_resistance import TestContactResistance, ResultadoContactResistance
from app.models.test_torque import TestTorque, ResultadoTorque

# Otros modelos
from app.models.project import Project
from app.models.test import Test
from app.models.equipment import Equipment
from app.models.test_realizados import TestRealizado  # ✅ Dashboard / My Tests

# Utilidades
from app.utils.pdf_generator import generar_pdf_test
from app.utils.correo import enviar_correo_con_pdf, obtener_correos_admins

import os
import shutil
from datetime import datetime
import json

router = APIRouter(prefix="/formulario", tags=["Form"])
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/guardar")
async def save_form(
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
    user_id = 1  # ✅ Luego será dinámico (usuario autenticado)

    # --- EQUIPMENT ---
    equipment_code = f"{location_1}-{equipment_type}-{number_equipment_type}".upper()
    equipment = db.query(Equipment).filter(Equipment.codigo == equipment_code).first()
    if not equipment:
        equipment = Equipment(
            codigo=equipment_code,
            tipo=equipment_type,
            numero_tipo_equipo=number_equipment_type,
            project_id=project_id
        )
        db.add(equipment)
        db.commit()
        db.refresh(equipment)

    # --- TEST GENERAL ---
    test_general = Test(project_id=project_id)
    db.add(test_general)
    db.commit()
    db.refresh(test_general)

    # ✅ --- REGISTER IN TEST_REALIZADOS ---
    new_test_done = TestRealizado(
        project_id=project_id,
        equipment_id=equipment.id,
        user_id=user_id,
        test_id=test_general.id,
        estado="Incompleto"
    )
    db.add(new_test_done)
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
                    "punto_prueba": r["punto_prueba"],
                    "path": path
                })

            result = result_model(
                test_id=test_instance.id,
                punto_prueba=r["punto_prueba"],
                resultado_valor=None if r["resultado_valor"] == "N/A" else float(r["resultado_valor"]),
                unidad=r["unidad"],
                observaciones=r.get("observaciones", ""),
                imagen=path,
                cable_set=r.get("cable_set"),
                tiempo_aplicado=float(r.get("tiempo_aplicado", 0)) if "tiempo_aplicado" in r else None,
                valor_nominal=float(r.get("valor_nominal", 0)) if "valor_nominal" in r else None,
                valor_comprobacion=float(r.get("valor_comprobacion", 0)) if "valor_comprobacion" in r else None
            )
            db.add(result)
        db.commit()

    # --- TEST SELECTION ---
    if test_type == "continuidad":
        save_results(TestContinuidad, ResultadoContinuidad)
    elif test_type == "megado":
        save_results(TestMegado, ResultadoMegado)
    elif test_type == "contact_resistance":
        save_results(TestContactResistance, ResultadoContactResistance)
    elif test_type == "torque":
        save_results(TestTorque, ResultadoTorque)
    else:
        raise HTTPException(status_code=400, detail="Test type not recognized")

    # --- PDF DATA ---
    project = db.query(Project).filter(Project.id == project_id).first()
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
        "user_name": "Technician",
        "logo_cliente": f"logo_cliente_{project.nombre}.png",
        "logo_subcontrata": f"logo_subcontrata_{project.nombre}.png"
    }
    pdf_results = [
        {
            "punto_prueba": r["punto_prueba"],
            "resultado_valor": r["resultado_valor"],
            "unidad": r["unidad"],
            "observaciones": r.get("observaciones", ""),
            "cable_set": r.get("cable_set"),
            "valor_nominal": r.get("valor_nominal"),
            "valor_comprobacion": r.get("valor_comprobacion")
        }
        for r in data_parsed
    ]

    # --- GENERATE PDF ---
    output_pdf_path = f"output/{test_type}_{equipment_code}.pdf"
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    generar_pdf_test(test_data, pdf_results, output_path=output_pdf_path)

    # --- SEND EMAIL ---
    emails = obtener_correos_admins(db, project_id)
    enviar_correo_con_pdf(
        destinatarios=emails,
        asunto=f"{test_type.capitalize()} - {equipment_code}",
        cuerpo=f"Report of {test_type} for equipment {equipment_code}",
        archivo_pdf=output_pdf_path
    )

    return {"message": "Form and results saved successfully"}
