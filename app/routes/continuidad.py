from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.parametros_continuidad import ParametroContinuidad
from app.schemas.parametros import ParametroContinuidadCreate, ParametroContinuidadUpdate
from app.utils.correo import obtener_correos_admins

router = APIRouter(prefix="/parametros/continuidad", tags=["Parametros Continuidad"])

@router.post("/crear")
def crear_parametro(parametro: ParametroContinuidadCreate, db: Session = Depends(get_db)):
    nuevo = ParametroContinuidad(**parametro.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/listar")
def listar_parametros(db: Session = Depends(get_db)):
    return db.query(ParametroContinuidad).all()

@router.put("/{parametro_id}/editar")
def editar_parametro(parametro_id: int, datos: ParametroContinuidadUpdate, db: Session = Depends(get_db)):
    parametro = db.query(ParametroContinuidad).filter(ParametroContinuidad.id == parametro_id).first()
    if not parametro:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(parametro, key, value)
    db.commit()
    return parametro

@router.delete("/{parametro_id}/eliminar")
def eliminar_parametro(parametro_id: int, db: Session = Depends(get_db)):
    parametro = db.query(ParametroContinuidad).filter(ParametroContinuidad.id == parametro_id).first()
    if not parametro:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")
    db.delete(parametro)
    db.commit()
    return {"mensaje": "Parámetro eliminado correctamente"}
