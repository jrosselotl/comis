from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.test_project import TestProject
from app.schemas.test_project import TestProjectCreate, TestProjectUpdate, TestProjectResponse

router = APIRouter(prefix="/test_project", tags=["Test Project"])

# ✅ Listar todos los tests asociados a un proyecto
@router.get("/{project_id}", response_model=List[TestProjectResponse])
def list_tests_for_project(project_id: int, db: Session = Depends(get_db)):
    return db.query(TestProject).filter(TestProject.project_id == project_id).all()

# ✅ Asociar un test a un proyecto
@router.post("/", response_model=TestProjectResponse)
def add_test_to_project(test_project: TestProjectCreate, db: Session = Depends(get_db)):
    existing = db.query(TestProject).filter(
        TestProject.project_id == test_project.project_id,
        TestProject.test_id == test_project.test_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Test already linked to this project")

    new_link = TestProject(**test_project.dict())
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link

# ✅ Activar/desactivar un test en un proyecto
@router.put("/{link_id}", response_model=TestProjectResponse)
def update_test_status(link_id: int, update_data: TestProjectUpdate, db: Session = Depends(get_db)):
    link = db.query(TestProject).filter(TestProject.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    link.active = update_data.active
    db.commit()
    db.refresh(link)
    return link

# ✅ Eliminar la relación
@router.delete("/{link_id}")
def delete_test_project(link_id: int, db: Session = Depends(get_db)):
    link = db.query(TestProject).filter(TestProject.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    db.delete(link)
    db.commit()
    return {"message": "Link removed successfully"}
