from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.proyecto import ProyectoCreate, ProyectoOut
from app.models.proyecto import Proyecto
from app.database import get_db

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

# Crear nuevo proyecto
@router.post("/", response_model=ProyectoOut)
def crear_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    nuevo = Proyecto(
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/proyectos/{proyecto_id}/tests")
def obtener_tests_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    relaciones = db.query(ProyectoTipoTest).filter_by(proyecto_id=proyecto_id).all()
    lista_tests = []
    for rel in relaciones:
        test = db.query(Test).filter_by(id=rel.tipo_test).first()
        if test:
            lista_tests.append({"id": test.id, "nombre": test.nombre})
    return lista_tests

# Obtener todos los proyectos
@router.get("/", response_model=list[ProyectoOut])
def listar_proyectos(db: Session = Depends(get_db)):
    return db.query(Proyecto).all()
