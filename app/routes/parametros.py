from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

from app.models.parametros_continuidad import ParametroContinuidad
from app.models.parametros_megado import ParametroMegado
from app.models.parametros_contact_resistance import ParametroContactResistance
from app.models.parametros_torque import ParametroTorque

from app.schemas.parametros_continuidad import (
    ParametroContinuidadCreate, ParametroContinuidadUpdate,
)
from app.schemas.parametros_megado import (
    ParametroMegadoCreate, ParametroMegadoUpdate,
)
from app.schemas.parametros_contact_resistance import (
    ParametroContactResistanceCreate, ParametroContactResistanceUpdate,
)
from app.schemas.parametros_torque import (
    ParametroTorqueCreate, ParametroTorqueUpdate,
)

router = APIRouter(prefix="/parametros", tags=["Parametros"])

TIPO_PARAMETROS = {
    "continuidad": (ParametroContinuidad, ParametroContinuidadCreate, ParametroContinuidadUpdate),
    "megado": (ParametroMegado, ParametroMegadoCreate, ParametroMegadoUpdate),
    "contact_resistance": (ParametroContactResistance, ParametroContactResistanceCreate, ParametroContactResistanceUpdate),
    "torque": (ParametroTorque, ParametroTorqueCreate, ParametroTorqueUpdate)
}

@router.post("/{tipo_test}/crear")
def crear_parametro(tipo_test: str, datos: dict, db: Session = Depends(get_db)):
    if tipo_test not in TIPO_PARAMETROS:
        raise HTTPException(status_code=400, detail="Tipo de prueba no válido")
    Modelo, SchemaCreate, _ = TIPO_PARAMETROS[tipo_test]
    parametro = Modelo(**SchemaCreate(**datos).dict())
    db.add(parametro)
    db.commit()
    db.refresh(parametro)
    return parametro

@router.get("/{tipo_test}/listar")
def listar_parametros(tipo_test: str, db: Session = Depends(get_db)):
    if tipo_test not in TIPO_PARAMETROS:
        raise HTTPException(status_code=400, detail="Tipo de prueba no válido")
    Modelo, _, _ = TIPO_PARAMETROS[tipo_test]
    return db.query(Modelo).all()

@router.put("/{tipo_test}/{parametro_id}/editar")
def editar_parametro(tipo_test: str, parametro_id: int, datos: dict, db: Session = Depends(get_db)):
    if tipo_test not in TIPO_PARAMETROS:
        raise HTTPException(status_code=400, detail="Tipo de prueba no válido")
    Modelo, _, SchemaUpdate = TIPO_PARAMETROS[tipo_test]
    parametro = db.query(Modelo).filter(Modelo.id == parametro_id).first()
    if not parametro:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")
    for key, value in SchemaUpdate(**datos).dict(exclude_unset=True).items():
        setattr(parametro, key, value)
    db.commit()
    return parametro

@router.delete("/{tipo_test}/{parametro_id}/eliminar")
def eliminar_parametro(tipo_test: str, parametro_id: int, db: Session = Depends(get_db)):
    if tipo_test not in TIPO_PARAMETROS:
        raise HTTPException(status_code=400, detail="Tipo de prueba no válido")
    Modelo, _, _ = TIPO_PARAMETROS[tipo_test]
    parametro = db.query(Modelo).filter(Modelo.id == parametro_id).first()
    if not parametro:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")
    db.delete(parametro)
    db.commit()
    return {"mensaje": "Parámetro eliminado correctamente"}
