from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_contact_resistance import TestContactResistance, ResultadoContactResistance
from app.models.test import Test
from app.models.equipment import Equipment
from app.models.project import Project
from app.utils.pdf_generator import generar_pdf_test
from app.utils.correo import enviar_correo_con_pdf, obtener_correos_admins

import os, shutil, json
from datetime import datetime

router = APIRouter(prefix="/formulario/contact_resistance", tags=["Formulario Contact Resistance"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/guardar")
async def guardar_test_contact_resistance(
    project_id: int = Form(...),
    ubicacion_1: str = Form(...),
    numero_ubicacion_1: str = Form(...),
    ubicacion_2: str = Form(None),
    numero_ubicacion_2: str = Form(None),
    tipo_equipo: str = Form(...),
    numero_tipo_equipo: str = Form(...),
    sub_equipo: str = Form(None),
    numero_sub_equipo: str = Form(None),
    tipo_prueba: str = Form(...),
    cable_sets: int = Form(...),
    tipo_alimentacion: str = Form(...),
    terminal: str = Form(None),
    datos: str = Form(...),
    imagenes: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    datos_parsed = json.loads(datos)
    user_id = 1  # 🔹 Se integrará autenticación real en el futuro

    # ✅ Generar código único del equipo
    codigo_equipo = f"{ubicacion_1}-{tipo_equipo}-{sub_equipo or 'GEN'}{numero_sub_equipo or ''}".upper()

    # ✅ Verificar o crear equipo
    equipo = db.query(Equipo).filter_by(codigo=codigo_equipo).first()
    if not equipo:
        equipo = Equipo(
            codigo=codigo_equipo,
            tipo=tipo_equipo,
            sub_equipo=sub_equipo,
            proyecto_id=proyecto_id
        )
        db.add(equipo)
        db.commit()
        db.refresh(equipo)

    # ✅ Crear registro en tabla general de tests
    test = Test(tipo_prueba=tipo_prueba, equipment_id=equipment.id)
    db.add(test)
    db.commit()
    db.refresh(test)

    # ✅ Crear test específico de contact resistance
    test_contact = TestContactResistance(
        equipment_id=equipment.id,
        user_id=user_id,
        test_id=test.id
    )
    db.add(test_contact)
    db.commit()
    db.refresh(test_contact)

    # ✅ Guardar resultados (sin parámetros ni validaciones)
    imagenes_info = []
    resultados_pdf = []

    for i, r in enumerate(datos_parsed):
        imagen = imagenes[i] if i < len(imagenes) else None
        filename = f"{codigo_equipo}_{r['punto_prueba']}_{i}.png" if imagen else None
        filepath = None

        if imagen:
            filepath = os.path.join(UPLOAD_DIR, filename)
            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(imagen.file, buffer)
            imagenes_info.append({
                "cable_set": r.get("cable_set"),
                "punto_prueba": r["punto_prueba"],
                "path": filepath
            })

        resultado = ResultadoContactResistance(
            test_id=test_contact.id,
            cable_set=r.get("cable_set"),
            punto_prueba=r["punto_prueba"],
            resultado_valor=None if r["resultado_valor"] == "N/A" else float(r["resultado_valor"]),
            unidad=r["unidad"],
            observaciones=r.get("observaciones"),
            imagen=filepath
        )
        db.add(resultado)

        resultados_pdf.append({
            "cable_set": r.get("cable_set"),
            "punto_prueba": r["punto_prueba"],
            "resultado_valor": r["resultado_valor"],
            "unidad": r["unidad"],
            "observaciones": r.get("observaciones", "")
        })

    db.commit()

    # ✅ Datos para PDF
    proyecto = db.query(Proyecto).filter_by(id=proyecto_id).first()
    detalles_equipo = {
        "Proyecto": project.nombre,
        "Ubicación Principal": f"{ubicacion_1} Nº{numero_ubicacion_1}",
        "Ubicación Secundaria": f"{ubicacion_2} Nº{numero_ubicacion_2}" if ubicacion_2 else "-",
        "Tipo de Equipo": f"{tipo_equipo} Nº{numero_tipo_equipo}",
        "Subequipo": f"{sub_equipo} Nº{numero_sub_equipo}" if sub_equipo else "-",
        "Tipo de Alimentación": tipo_alimentacion,
        "Terminal": terminal
    }

    test_data = {
        "equipment_id": codigo_equipo,
        "tipo_prueba": tipo_prueba,
        "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "detalles_equipo": detalles_equipo,
        "imagenes": imagenes_info,
        "logo_cliente": f"logo_cliente_{project.nombre}.png",
        "logo_subcontrata": f"logo_subcontrata_{project.nombre}.png",
        "nombre_usuario": "Técnico"
    }

    # ✅ Generar PDF
    output_pdf_path = f"output/{tipo_prueba}_{codigo_equipo}.pdf"
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    generar_pdf_test(test_data, resultados_pdf, output_path=output_pdf_path)

    # ✅ Enviar correo
    correos_destino = obtener_correos_admins(db, project_id)
    enviar_correo_con_pdf(
        destinatarios=correos_destino,
        asunto=f"{tipo_prueba.capitalize()} - {codigo_equipo}",
        cuerpo=f"Informe de {tipo_prueba} para el equipo {codigo_equipo}",
        archivo_pdf=output_pdf_path
    )

    return {"mensaje": "Formulario y resultados guardados correctamente"}
