from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os, shutil, json
from datetime import datetime
from app.database import get_db
from app.models.test_megado import TestMegado, ResultadoMegado
from app.models.parametros_megado import ParametrosMegado
from app.models.tests import Test
from app.models.equipo import Equipo
from app.utils.pdf_generator import generar_pdf_test
from app.utils.correo import enviar_correo_con_pdf
from app.utils.correo import obtener_correos_admins

router = APIRouter(prefix="/megado", tags=["Test Megado"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def evaluar_aprobado(logica: str, referencia: float, valor: float) -> str:
    if valor is None:
        return "No"
    try:
        if logica == "mayor_que":
            return "Sí" if valor > referencia else "No"
        elif logica == "menor_que":
            return "Sí" if valor < referencia else "No"
        elif logica == "igual":
            return "Sí" if valor == referencia else "No"
    except:
        return "No"
    return "No"

@router.post("/guardar")
async def guardar_test_megado(
    proyecto_id: int = Form(...),
    equipo_id: int = Form(...),
    usuario_id: int = Form(...),
    datos: str = Form(...),
    imagenes: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    datos_parsed = json.loads(datos)
    equipo = db.query(Equipo).filter_by(id=equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    nuevo_test = Test(usuario_id=usuario_id, proyecto_id=proyecto_id, tipo_prueba="megado")
    db.add(nuevo_test)
    db.commit()
    db.refresh(nuevo_test)

    test_megado = TestMegado(equipo_id=equipo_id, usuario_id=usuario_id, test_id=nuevo_test.id)
    db.add(test_megado)
    db.commit()
    db.refresh(test_megado)

    parametros = db.query(ParametrosMegado).filter_by(proyecto_id=proyecto_id).all()
    imagenes_info = []
    index = 0

    for dato in datos_parsed:
        punto = dato["punto_prueba"]
        cable_set = dato.get("cable_set", 0)
        valor = dato.get("resultado_valor")
        unidad = dato.get("unidad", "")
        observaciones = dato.get("observaciones", "")

        param = next((p for p in parametros if p.punto == punto and p.cable_set == cable_set), None)
        if not param:
            aprobado = "No"
        else:
            aprobado = evaluar_aprobado(param.logica, param.referencia, valor)

        nombre_archivo = None
        if imagenes and index < len(imagenes):
            imagen = imagenes[index]
            if imagen.filename:
                nombre_archivo = f"{datetime.utcnow().timestamp()}_{imagen.filename}"
                ruta_archivo = os.path.join(UPLOAD_DIR, nombre_archivo)
                with open(ruta_archivo, "wb") as f:
                    shutil.copyfileobj(imagen.file, f)
                imagenes_info.append(nombre_archivo)
            else:
                imagenes_info.append("")
            index += 1
        else:
            imagenes_info.append("")

        resultado = ResultadoMegado(
            test_id=test_megado.id,
            punto=punto,
            resultado_valor=valor,
            unidad=unidad,
            aprobado=aprobado,
            observaciones=observaciones,
            imagen=nombre_archivo
        )
        db.add(resultado)

    db.commit()

    # PDF
    proyecto = equipo.proyecto
    nombre_equipo = equipo.codigo
    detalles_equipo = {
        "Proyecto": proyecto.nombre,
        "Ubicación Principal": equipo.ubicacion_1,
        "Ubicación Secundaria": equipo.ubicacion_2 or "-",
        "Tipo de Equipo": equipo.tipo_equipo,
        "Subequipo": equipo.sub_equipo or "-",
        "Tipo de Alimentación": equipo.tipo_alimentacion
    }

    test_data = {
        "tipo_prueba": "megado",
        "equipo_id": nombre_equipo,
        "fecha": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "detalles_equipo": detalles_equipo,
        "imagenes": imagenes_info,
        "nombre_usuario": equipo.usuario.nombre if equipo.usuario else "Desconocido",
        "logo_cliente": f"logo_cliente_{proyecto.nombre}.png",
        "logo_subcontrata": f"logo_subcontrata_{proyecto.nombre}.png"
    }

    resultados_pdf = [
        {
            "punto_prueba": r["punto_prueba"],
            "referencia_valor": param.referencia if param else "-",
            "resultado_valor": r["resultado_valor"],
            "aprobado": evaluar_aprobado(param.logica, param.referencia, r["resultado_valor"]) if param else "No",
            "observaciones": r.get("observaciones", ""),
            "cable_set": r.get("cable_set", "")
        }
        for r in datos_parsed
        for param in parametros if param.punto == r["punto_prueba"] and param.cable_set == r.get("cable_set")
    ]

    output_pdf_path = f"output/megado_{nombre_equipo}.pdf"
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    generar_pdf_test(test_data, resultados_pdf, output_path=output_pdf_path)
    
    correos_destino = obtener_correos_admins(db, proyecto_id)
    
    enviar_correo_con_pdf(
        destinatarios=correos_destino,
        asunto=f"Megado - {nombre_equipo}",
        cuerpo=f"Informe de megado para el equipo {nombre_equipo}",
        archivo_pdf=output_pdf_path
    )
    return {"mensaje": "Prueba de megado guardada correctamente"}
