from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_megado import TestMegado, ResultadoMegado
from app.models.test import Test
from app.models.equipo import Equipo
from app.models.proyecto import Proyecto
from app.utils.pdf_generator import generar_pdf_test
from app.utils.correo import enviar_correo_con_pdf, obtener_correos_admins

import os, shutil, json
from datetime import datetime

router = APIRouter(prefix="/formulario/megado", tags=["Formulario Megado"])
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/guardar")
async def guardar_test_megado(
    proyecto_id: int = Form(...),
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
    usuario_id = 1  # 🔹 Se integrará autenticación real en el futuro

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

    # ✅ Crear test general
    test = Test(tipo_prueba=tipo_prueba, equipo_id=equipo.id)
    db.add(test)
    db.commit()
    db.refresh(test)

    # ✅ Crear test específico de megado
    test_meg = TestMegado(
        equipo_id=equipo.id,
        usuario_id=usuario_id,
        test_id=test.id
    )
    db.add(test_meg)
    db.commit()
    db.refresh(test_meg)

    # ✅ Guardar resultados (sin parámetros ni lógica de aprobado)
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
                "path": filepath,
                "punto_prueba": r["punto_prueba"],
                "cable_set": r.get("cable_set")
            })

        resultado = ResultadoMegado(
            test_id=test_meg.id,
            punto=r['punto_prueba'],
            resultado_valor=None if r['resultado_valor'] == "N/A" else float(r['resultado_valor']),
            unidad=r['unidad'],
            tiempo_aplicado=float(r.get('tiempo_aplicado', 0)),  # 🔹 Ahora el técnico lo ingresa manualmente
            observaciones=r.get('observaciones'),
            imagen=filepath,
            cable_set=r.get("cable_set")
        )
        db.add(resultado)

        resultados_pdf.append({
            "punto_prueba": r["punto_prueba"],
            "resultado_valor": r["resultado_valor"],
            "unidad": r["unidad"],
            "tiempo_aplicado": r.get('tiempo_aplicado', 0),
            "observaciones": r.get("observaciones", ""),
            "cable_set": r.get("cable_set")
        })

    db.commit()

    # ✅ Datos para PDF
    proyecto = db.query(Proyecto).filter_by(id=proyecto_id).first()
    detalles_equipo = {
        "Proyecto": proyecto.nombre,
        "Ubicación Principal": f"{ubicacion_1} Nº{numero_ubicacion_1}",
        "Ubicación Secundaria": f"{ubicacion_2} Nº{numero_ubicacion_2}" if ubicacion_2 else "-",
        "Tipo de Equipo": f"{tipo_equipo} Nº{numero_tipo_equipo}",
        "Subequipo": f"{sub_equipo} Nº{numero_sub_equipo}" if sub_equipo else "-",
        "Tipo de Alimentación": tipo_alimentacion,
        "Terminal": terminal
    }

    test_data = {
        "equipo_id": codigo_equipo,
        "tipo_prueba": tipo_prueba,
        "fecha": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "detalles_equipo": detalles_equipo,
        "imagenes": imagenes_info,
        "logo_cliente": f"logo_cliente_{proyecto.nombre}.png",
        "logo_subcontrata": f"logo_subcontrata_{proyecto.nombre}.png",
        "nombre_usuario": "Técnico"
    }

    # ✅ Generar PDF
    output_pdf_path = f"output/{tipo_prueba}_{codigo_equipo}.pdf"
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    generar_pdf_test(test_data, resultados_pdf, output_path=output_pdf_path)

    # ✅ Enviar correo
    correos_destino = obtener_correos_admins(db, proyecto_id)
    enviar_correo_con_pdf(
        destinatarios=correos_destino,
        asunto=f"{tipo_prueba.capitalize()} - {codigo_equipo}",
        cuerpo=f"Informe de {tipo_prueba} para el equipo {codigo_equipo}",
        archivo_pdf=output_pdf_path
    )

    return {"mensaje": "Formulario y resultados guardados correctamente"}
