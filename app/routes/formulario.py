from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_continuidad import TestContinuidad, ResultadoContinuidad
from app.models.test_megado import TestMegado, ResultadoMegado
from app.models.parametros_continuidad import ParametroContinuidad
from app.models.parametros_megado import ParametroMegado
from app.models.proyecto import Proyecto
from app.models.usuario import Usuario
from app.models.test import Test
from app.models.equipo import Equipo
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

    # Equipo
    codigo_equipo = f"{ubicacion_1}-{tipo_equipo}-{numero_tipo_equipo}"
    equipo = db.query(Equipo).filter(Equipo.codigo == codigo_equipo).first()
    if not equipo:
        equipo = Equipo(codigo=codigo_equipo, tipo=tipo_equipo, numero=numero_tipo_equipo)
        db.add(equipo)
        db.commit()
        db.refresh(equipo)

    # Test general
    test_general = Test(proyecto_id=proyecto_id)
    db.add(test_general)
    db.commit()
    db.refresh(test_general)

    # Imágenes
    imagenes_info = []
    img_iter = iter(imagenes)

    if tipo_prueba == "continuidad":
        test = TestContinuidad(equipo_id=equipo.id, test_id=test_general.id, usuario_id=1)
        db.add(test)
        db.commit()
        db.refresh(test)

        parametros = db.query(ParametroContinuidad).filter(ParametroContinuidad.proyecto_id == proyecto_id).all()
        dict_param = {(p.cable_set, p.punto): p for p in parametros}

        for r in datos_parsed:
            param = dict_param.get((r["cable_set"], r["punto_prueba"]))
            aprobado = "No"
            if r["resultado_valor"] == "N/A":
                aprobado = "Sí"
            elif param:
                if param.logica == "mayor_que" and float(r["resultado_valor"]) > float(param.referencia):
                    aprobado = "Sí"
                elif param.logica == "menor_que" and float(r["resultado_valor"]) < float(param.referencia):
                    aprobado = "Sí"

            imagen = next(img_iter, None)
            filename = f"{datetime.utcnow().timestamp()}_{imagen.filename}" if imagen else None
            if imagen:
                path = os.path.join(UPLOAD_DIR, filename)
                with open(path, "wb") as f:
                    shutil.copyfileobj(imagen.file, f)
                imagenes_info.append(path)

            resultado = ResultadoContinuidad(
                test_id=test.id,
                punto=r["punto_prueba"],
                resultado_valor=None if r["resultado_valor"] == "N/A" else float(r["resultado_valor"]),
                unidad=r["unidad"],
                aprobado=aprobado,
                observaciones=r.get("observaciones", ""),
                imagen=filename
            )
            db.add(resultado)
        db.commit()

    elif tipo_prueba == "megado":
        test = TestMegado(equipo_id=equipo.id, test_id=test_general.id, usuario_id=1)
        db.add(test)
        db.commit()
        db.refresh(test)

        parametros = db.query(ParametroMegado).filter(ParametroMegado.proyecto_id == proyecto_id).all()
        dict_param = {(p.cable_set, p.punto): p for p in parametros}

        for r in datos_parsed:
            param = dict_param.get((r["cable_set"], r["punto_prueba"]))
            aprobado = "No"
            if r["resultado_valor"] == "N/A":
                aprobado = "Sí"
            elif param:
                if param.logica == "mayor_que" and float(r["resultado_valor"]) > float(param.referencia):
                    aprobado = "Sí"
                elif param.logica == "menor_que" and float(r["resultado_valor"]) < float(param.referencia):
                    aprobado = "Sí"

            imagen = next(img_iter, None)
            filename = f"{datetime.utcnow().timestamp()}_{imagen.filename}" if imagen else None
            if imagen:
                path = os.path.join(UPLOAD_DIR, filename)
                with open(path, "wb") as f:
                    shutil.copyfileobj(imagen.file, f)
                imagenes_info.append(path)

            resultado = ResultadoMegado(
                test_id=test.id,
                punto=r["punto_prueba"],
                resultado_valor=None if r["resultado_valor"] == "N/A" else float(r["resultado_valor"]),
                unidad=r["unidad"],
                aprobado=aprobado,
                tiempo_aplicado=float(r.get("tiempo_aplicado", 0)),
                observaciones=r.get("observaciones", ""),
                imagen=filename
            )
            db.add(resultado)
        db.commit()

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
        "observaciones": "",
        "detalles_equipo": detalles_equipo,
        "imagenes": imagenes_info,
        "nombre_usuario": "Técnico",  # Puedes enlazar al usuario si implementas auth
        "logo_cliente": f"logo_cliente_{proyecto.nombre}.png",
        "logo_subcontrata": f"logo_subcontrata_{proyecto.nombre}.png"
    }

    resultados_pdf = [
        {
            "punto_prueba": r["punto_prueba"],
            "referencia_valor": r["referencia_valor"],
            "resultado_valor": r["resultado_valor"],
            "unidad": r["unidad"],
            "aprobado": "Sí" if r["resultado_valor"] == "N/A" else aprobado,
            "observaciones": r.get("observaciones", ""),
            "cable_set": r.get("cable_set")
        }
        for r in datos_parsed
    ]

    output_pdf_path = f"output/{tipo_prueba}_{codigo_equipo}.pdf"
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    generar_pdf_test(test_data, resultados_pdf, output_path=output_pdf_path)

    correos_destino = obtener_correos_admins(db, proyecto_id)
    enviar_correo_con_pdf(
        destinatarios=correos_destino,
        asunto=f"{tipo_prueba.capitalize()} - {codigo_equipo}",
        cuerpo=f"Informe de {tipo_prueba} para el equipo {codigo_equipo}",
        archivo_pdf=output_pdf_path
    )

    return {"mensaje": "Formulario y resultados guardados correctamente"}
