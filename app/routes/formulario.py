from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

# Modelos de pruebas
from app.models.test_continuidad import TestContinuidad, ResultadoContinuidad
from app.models.test_megado import TestMegado, ResultadoMegado
from app.models.test_contact_resistance import TestContactResistance, ResultadoContactResistance
from app.models.test_torque import TestTorque, ResultadoTorque

# Otros modelos
from app.models.proyecto import Proyecto
from app.models.usuario import Usuario
from app.models.test import Test
from app.models.equipo import Equipo

# Utilidades
from app.utils.pdf_generator import generar_pdf_test
from app.utils.correo import enviar_correo_con_pdf, obtener_correos_admins

import os
import shutil
from datetime import datetime
import json

router = APIRouter(prefix="/formulario", tags=["Formulario"])
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/guardar")
async def guardar_formulario(
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

    # --- EQUIPO ---
    codigo_equipo = f"{ubicacion_1}-{tipo_equipo}-{numero_tipo_equipo}"
    equipo = db.query(Equipo).filter(Equipo.codigo == codigo_equipo).first()
    if not equipo:
        equipo = Equipo(codigo=codigo_equipo, tipo=tipo_equipo, numero=numero_tipo_equipo)
        db.add(equipo)
        db.commit()
        db.refresh(equipo)

    # --- TEST GENERAL ---
    test_general = Test(proyecto_id=proyecto_id)
    db.add(test_general)
    db.commit()
    db.refresh(test_general)

    # --- IMÁGENES ---
    imagenes_info = []
    img_iter = iter(imagenes)

    # --- FUNCIÓN GENÉRICA PARA GUARDAR RESULTADOS ---
    def guardar_resultados(modelo_test, modelo_resultado):
        test = modelo_test(equipo_id=equipo.id, test_id=test_general.id, usuario_id=1)
        db.add(test)
        db.commit()
        db.refresh(test)

        for r in datos_parsed:
            imagen = next(img_iter, None)
            filename = f"{datetime.utcnow().timestamp()}_{imagen.filename}" if imagen else None
            if imagen:
                path = os.path.join(UPLOAD_DIR, filename)
                with open(path, "wb") as f:
                    shutil.copyfileobj(imagen.file, f)
                imagenes_info.append(path)

            resultado = modelo_resultado(
                test_id=test.id,
                punto=r["punto_prueba"],
                resultado_valor=None if r["resultado_valor"] == "N/A" else float(r["resultado_valor"]),
                unidad=r["unidad"],
                observaciones=r.get("observaciones", ""),
                imagen=filename,
                cable_set=r.get("cable_set"),
                tiempo_aplicado=float(r.get("tiempo_aplicado", 0)) if "tiempo_aplicado" in r else None,
                valor_nominal=float(r.get("valor_nominal", 0)) if "valor_nominal" in r else None,
                valor_comprobacion=float(r.get("valor_comprobacion", 0)) if "valor_comprobacion" in r else None
            )
            db.add(resultado)
        db.commit()

    # --- SELECCIÓN DE PRUEBA ---
    if tipo_prueba == "continuidad":
        guardar_resultados(TestContinuidad, ResultadoContinuidad)
    elif tipo_prueba == "megado":
        guardar_resultados(TestMegado, ResultadoMegado)
    elif tipo_prueba == "contact_resistance":
        guardar_resultados(TestContactResistance, ResultadoContactResistance)
    elif tipo_prueba == "torque":
        guardar_resultados(TestTorque, ResultadoTorque)
    else:
        raise HTTPException(status_code=400, detail="Tipo de prueba no reconocido")

    # --- DATOS PARA PDF ---
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()

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
        "nombre_usuario": "Técnico",
        "logo_cliente": f"logo_cliente_{proyecto.nombre}.png",
        "logo_subcontrata": f"logo_subcontrata_{proyecto.nombre}.png"
    }

    resultados_pdf = [
        {
            "punto_prueba": r["punto_prueba"],
            "resultado_valor": r["resultado_valor"],
            "unidad": r["unidad"],
            "observaciones": r.get("observaciones", ""),
            "cable_set": r.get("cable_set"),
            "valor_nominal": r.get("valor_nominal", None),
            "valor_comprobacion": r.get("valor_comprobacion", None)
        }
        for r in datos_parsed
    ]

    # --- GENERAR PDF ---
    output_pdf_path = f"output/{tipo_prueba}_{codigo_equipo}.pdf"
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    generar_pdf_test(test_data, resultados_pdf, output_path=output_pdf_path)

    # --- ENVIAR POR CORREO ---
    correos_destino = obtener_correos_admins(db, proyecto_id)
    enviar_correo_con_pdf(
        destinatarios=correos_destino,
        asunto=f"{tipo_prueba.capitalize()} - {codigo_equipo}",
        cuerpo=f"Informe de {tipo_prueba} para el equipo {codigo_equipo}",
        archivo_pdf=output_pdf_path
    )

    return {"mensaje": "Formulario y resultados guardados correctamente"}
