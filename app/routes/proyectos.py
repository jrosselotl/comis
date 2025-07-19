from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.project import ProjectCreate, ProjectOut
from app.models.project import Project
from app.models.test import Test
from app.database import get_db

router = APIRouter(prefix="/projects", tags=["Projects"])

# Create new project
@router.post("/", response_model=ProjectOut)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Project(
        nombre=project.nombre,
        descripcion=project.descripcion
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# Get all projects
@router.get("/", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

# Get available tests for a project
@router.get("/{project_id}/tests")
def get_project_tests(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db.query(Test).filter(Test.project_id == project_id).all()

# Alias for frontend compatibility
@router.get("/list")
def alias_list_projects(db: Session = Depends(get_db)):
    return list_projects(db)
