from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.parametros_continuidad import ParametroContinuidad
from app.models.parametros_megado import ParametroMegado

router = APIRouter(prefix="/parametros", tags=["Parámetros"])

MODELOS = {
    "continuidad": ParametroContinuidad,
    "megado": ParametroMegado
}

@router.post("/{tipo_test}/crear")
def crear_parametro(tipo_test: str, datos: dict, db: Session = Depends(get_db)):
    modelo = MODELOS.get(tipo_test)
    if not modelo:
        raise HTTPException(status_code=400, detail="Tipo de test inválido")

    nuevo = modelo(**datos)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/{tipo_test}/listar")
def listar_parametros(tipo_test: str, db: Session = Depends(get_db)):
    modelo = MODELOS.get(tipo_test)
    if not modelo:
        raise HTTPException(status_code=400, detail="Tipo de test inválido")
    return db.query(modelo).all()

@router.put("/{tipo_test}/{id}/editar")
def editar_parametro(tipo_test: str, id: int, datos: dict, db: Session = Depends(get_db)):
    modelo = MODELOS.get(tipo_test)
    if not modelo:
        raise HTTPException(status_code=400, detail="Tipo de test inválido")
    
    param = db.query(modelo).get(id)
    if not param:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")
    
    for k, v in datos.items():
        setattr(param, k, v)
    
    db.commit()
    return {"ok": True}

@router.delete("/{tipo_test}/{id}/eliminar")
def eliminar_parametro(tipo_test: str, id: int, db: Session = Depends(get_db)):
    modelo = MODELOS.get(tipo_test)
    if not modelo:
        raise HTTPException(status_code=400, detail="Tipo de test inválido")
    
    param = db.query(modelo).get(id)
    if not param:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")

    db.delete(param)
    db.commit()
    return {"ok": True}
