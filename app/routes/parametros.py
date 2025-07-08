from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.parametros_continuidad import ParametrosContinuidad
from app.models.parametros_megado import ParametrosMegado

router = APIRouter(prefix="/parametros", tags=["Parámetros"])

MODELOS = {
    "continuidad": ParametrosContinuidad,
    "megado": ParametrosMegado
}

@router.post("/{tipo_test}/crear")
async def crear_parametro(tipo_test: str, request: Request, db: Session = Depends(get_db)):
    modelo = MODELOS.get(tipo_test)
    if not modelo:
        raise HTTPException(status_code=400, detail="Tipo de test inválido")

    data = await request.json()
    nuevo = modelo(**data)
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
async def editar_parametro(tipo_test: str, id: int, request: Request, db: Session = Depends(get_db)):
    modelo = MODELOS.get(tipo_test)
    if not modelo:
        raise HTTPException(status_code=400, detail="Tipo de test inválido")

    parametro = db.query(modelo).get(id)
    if not parametro:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")

    data = await request.json()
    for campo, valor in data.items():
        setattr(parametro, campo, valor)

    db.commit()
    return {"success": True}

@router.delete("/{tipo_test}/{id}/eliminar")
def eliminar_parametro(tipo_test: str, id: int, db: Session = Depends(get_db)):
    modelo = MODELOS.get(tipo_test)
    if not modelo:
        raise HTTPException(status_code=400, detail="Tipo de test inválido")

    parametro = db.query(modelo).get(id)
    if not parametro:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")

    db.delete(parametro)
    db.commit()
    return {"success": True}
