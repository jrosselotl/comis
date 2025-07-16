# app/routes/parametros.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.parametros_continuidad import ParametroContinuidad
from app.models.parametros_megado import ParametroMegado
from app.models.parametros_contact_resistance import ParametroContactResistance
from app.models.parametros_torque import ParametroTorque
from app.models.proyecto import Proyecto
from app.models.test import Test

router = APIRouter(prefix="/parametros", tags=["Parámetros Técnicos"])

# Diccionario para asociar modelos con tipos de test
PARAM_MODELS = {
    "continuidad": ParametroContinuidad,
    "megado": ParametroMegado,
    "contact_resistance": ParametroContactResistance,
    "torque": ParametroTorque
}

# ✅ Crear parámetro
@router.post("/{tipo_test}/crear")
def crear_parametro(tipo_test: str, data: dict, db: Session = Depends(get_db)):
    if tipo_test not in PARAM_MODELS:
        raise HTTPException(status_code=400, detail="Tipo de test no válido")

    modelo = PARAM_MODELS[tipo_test]
    nuevo = modelo(
        proyecto_id=data.get("proyecto_id"),
        ubicacion_1=data.get("ubicacion_1"),
        numero_ubicacion_1=data.get("numero_ubicacion_1"),
        ubicacion_2=data.get("ubicacion_2"),
        numero_ubicacion_2=data.get("numero_ubicacion_2"),
        tipo_equipo=data.get("tipo_equipo"),
        numero_tipo_equipo=data.get("numero_tipo_equipo"),
        sub_equipo=data.get("sub_equipo"),
        numero_sub_equipo=data.get("numero_sub_equipo"),
        referencia=data.get("referencia"),
        logica=data.get("logica"),
        unidad=data.get("unidad"),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"mensaje": f"Parámetro de {tipo_test} creado correctamente", "id": nuevo.id}

# ✅ Listar parámetros
@router.get("/{tipo_test}/listar")
def listar_parametros(tipo_test: str, db: Session = Depends(get_db)):
    if tipo_test not in PARAM_MODELS:
        raise HTTPException(status_code=400, detail="Tipo de test no válido")

    modelo = PARAM_MODELS[tipo_test]
    parametros = db.query(modelo).all()
    resultado = []
    for p in parametros:
        proyecto = db.query(Proyecto).filter(Proyecto.id == p.proyecto_id).first()
        resultado.append({
            "id": p.id,
            "proyecto_nombre": proyecto.nombre if proyecto else "Sin proyecto",
            "proyecto_id": p.proyecto_id,
            "tipo_test": tipo_test,
            "ubicacion_1": p.ubicacion_1,
            "numero_ubicacion_1": p.numero_ubicacion_1,
            "ubicacion_2": p.ubicacion_2,
            "numero_ubicacion_2": p.numero_ubicacion_2,
            "tipo_equipo": p.tipo_equipo,
            "numero_tipo_equipo": p.numero_tipo_equipo,
            "sub_equipo": p.sub_equipo,
            "numero_sub_equipo": p.numero_sub_equipo,
            "referencia": p.referencia,
            "logica": p.logica,
            "unidad": p.unidad,
        })
    return resultado

# ✅ Obtener un parámetro específico (para edición)
@router.get("/{tipo_test}/{id}/listar")
def obtener_parametro(tipo_test: str, id: int, db: Session = Depends(get_db)):
    if tipo_test not in PARAM_MODELS:
        raise HTTPException(status_code=400, detail="Tipo de test no válido")

    modelo = PARAM_MODELS[tipo_test]
    p = db.query(modelo).filter(modelo.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")

    return {
        "id": p.id,
        "proyecto_id": p.proyecto_id,
        "tipo_test": tipo_test,
        "ubicacion_1": p.ubicacion_1,
        "numero_ubicacion_1": p.numero_ubicacion_1,
        "ubicacion_2": p.ubicacion_2,
        "numero_ubicacion_2": p.numero_ubicacion_2,
        "tipo_equipo": p.tipo_equipo,
        "numero_tipo_equipo": p.numero_tipo_equipo,
        "sub_equipo": p.sub_equipo,
        "numero_sub_equipo": p.numero_sub_equipo,
        "referencia": p.referencia,
        "logica": p.logica,
        "unidad": p.unidad,
    }

# ✅ Editar parámetro
@router.put("/{tipo_test}/{id}/editar")
def editar_parametro(tipo_test: str, id: int, data: dict, db: Session = Depends(get_db)):
    if tipo_test not in PARAM_MODELS:
        raise HTTPException(status_code=400, detail="Tipo de test no válido")

    modelo = PARAM_MODELS[tipo_test]
    p = db.query(modelo).filter(modelo.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")

    for campo, valor in data.items():
        if hasattr(p, campo) and valor is not None:
            setattr(p, campo, valor)

    db.commit()
    db.refresh(p)
    return {"mensaje": f"Parámetro {id} de {tipo_test} editado correctamente"}

# ✅ Eliminar parámetro
@router.delete("/{tipo_test}/{id}/eliminar")
def eliminar_parametro(tipo_test: str, id: int, db: Session = Depends(get_db)):
    if tipo_test not in PARAM_MODELS:
        raise HTTPException(status_code=400, detail="Tipo de test no válido")

    modelo = PARAM_MODELS[tipo_test]
    p = db.query(modelo).filter(modelo.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")

    db.delete(p)
    db.commit()
    return {"mensaje": f"Parámetro {id} de {tipo_test} eliminado correctamente"}
