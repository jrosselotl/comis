from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.parametros_continuidad import ParametrosContinuidad
from app.models.parametros_megado import ParametrosMegado
from app.models.parametros_contact_resistance import ParametrosContactResistance
from app.models.parametros_torque import ParametrosTorque
from app.schemas.parametros_continuidad import ParametrosContinuidadCreate, ParametrosContinuidadOut
from app.schemas.parametros_megado import ParametrosMegadoCreate, ParametrosMegadoOut
from app.schemas.parametros_contact_resistance import ParametrosContactResistanceCreate, ParametrosContactResistanceOut
from app.schemas.parametros_torque import ParametrosTorqueCreate, ParametrosTorqueOut

router = APIRouter(prefix="/parametros", tags=["Parametros"])

# CONTINUIDAD
@router.post("/continuidad/crear", response_model=ParametrosContinuidadOut)
def crear_parametros_continuidad(param: ParametrosContinuidadCreate, db: Session = Depends(get_db)):
    nuevo = ParametrosContinuidad(**param.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/continuidad/listar", response_model=list[ParametrosContinuidadOut])
def listar_parametros_continuidad(db: Session = Depends(get_db)):
    return db.query(ParametrosContinuidad).all()

@router.put("/continuidad/{id}/editar", response_model=ParametrosContinuidadOut)
def editar_parametros_continuidad(id: int, param: ParametrosContinuidadCreate, db: Session = Depends(get_db)):
    existente = db.query(ParametrosContinuidad).filter_by(id=id).first()
    if not existente:
        raise HTTPException(status_code=404, detail="No encontrado")
    for k, v in param.dict().items():
        setattr(existente, k, v)
    db.commit()
    db.refresh(existente)
    return existente

@router.delete("/continuidad/{id}/eliminar")
def eliminar_parametros_continuidad(id: int, db: Session = Depends(get_db)):
    existente = db.query(ParametrosContinuidad).filter_by(id=id).first()
    if not existente:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(existente)
    db.commit()
    return {"mensaje": "Eliminado correctamente"}

# MEGADO
@router.post("/megado/crear", response_model=ParametrosMegadoOut)
def crear_parametros_megado(param: ParametrosMegadoCreate, db: Session = Depends(get_db)):
    nuevo = ParametrosMegado(**param.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/megado/listar", response_model=list[ParametrosMegadoOut])
def listar_parametros_megado(db: Session = Depends(get_db)):
    return db.query(ParametrosMegado).all()

@router.put("/megado/{id}/editar", response_model=ParametrosMegadoOut)
def editar_parametros_megado(id: int, param: ParametrosMegadoCreate, db: Session = Depends(get_db)):
    existente = db.query(ParametrosMegado).filter_by(id=id).first()
    if not existente:
        raise HTTPException(status_code=404, detail="No encontrado")
    for k, v in param.dict().items():
        setattr(existente, k, v)
    db.commit()
    db.refresh(existente)
    return existente

@router.delete("/megado/{id}/eliminar")
def eliminar_parametros_megado(id: int, db: Session = Depends(get_db)):
    existente = db.query(ParametrosMegado).filter_by(id=id).first()
    if not existente:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(existente)
    db.commit()
    return {"mensaje": "Eliminado correctamente"}

# CONTACT RESISTANCE
@router.post("/contact_resistance/crear", response_model=ParametrosContactResistanceOut)
def crear_parametros_contact(param: ParametrosContactResistanceCreate, db: Session = Depends(get_db)):
    nuevo = ParametrosContactResistance(**param.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/contact_resistance/listar", response_model=list[ParametrosContactResistanceOut])
def listar_parametros_contact(db: Session = Depends(get_db)):
    return db.query(ParametrosContactResistance).all()

@router.put("/contact_resistance/{id}/editar", response_model=ParametrosContactResistanceOut)
def editar_parametros_contact(id: int, param: ParametrosContactResistanceCreate, db: Session = Depends(get_db)):
    existente = db.query(ParametrosContactResistance).filter_by(id=id).first()
    if not existente:
        raise HTTPException(status_code=404, detail="No encontrado")
    for k, v in param.dict().items():
        setattr(existente, k, v)
    db.commit()
    db.refresh(existente)
    return existente

@router.delete("/contact_resistance/{id}/eliminar")
def eliminar_parametros_contact(id: int, db: Session = Depends(get_db)):
    existente = db.query(ParametrosContactResistance).filter_by(id=id).first()
    if not existente:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(existente)
    db.commit()
    return {"mensaje": "Eliminado correctamente"}

# TORQUE
@router.post("/torque/crear", response_model=ParametrosTorqueOut)
def crear_parametros_torque(param: ParametrosTorqueCreate, db: Session = Depends(get_db)):
    nuevo = ParametrosTorque(**param.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/torque/listar", response_model=list[ParametrosTorqueOut])
def listar_parametros_torque(db: Session = Depends(get_db)):
    return db.query(ParametrosTorque).all()

@router.put("/torque/{id}/editar", response_model=ParametrosTorqueOut)
def editar_parametros_torque(id: int, param: ParametrosTorqueCreate, db: Session = Depends(get_db)):
    existente = db.query(ParametrosTorque).filter_by(id=id).first()
    if not existente:
        raise HTTPException(status_code=404, detail="No encontrado")
    for k, v in param.dict().items():
        setattr(existente, k, v)
    db.commit()
    db.refresh(existente)
    return existente

@router.delete("/torque/{id}/eliminar")
def eliminar_parametros_torque(id: int, db: Session = Depends(get_db)):
    existente = db.query(ParametrosTorque).filter_by(id=id).first()
    if not existente:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(existente)
    db.commit()
    return {"mensaje": "Eliminado correctamente"}
