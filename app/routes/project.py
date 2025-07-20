from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.project import ProjectCreate, ProjectOut
from app.models.project import Project
from app.models.test import Test
from app.database import get_db

router = APIRouter(prefix="/project", tags=["Project"])

# Create new project
@router.post("/", response_model=ProjectOut)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Project(
        name=project.name,
        description=project.description
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# Get all project
@router.get("/", response_model=list[ProjectOut])
def list_project(db: Session = Depends(get_db)):
    return db.query(Project).all()

# Get available test for a project
@router.get("/{project_id}/test")
def get_project_test(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db.query(Test).filter(Test.project_id == project_id).all()

# Alias for frontend compatibility
@router.get("/list")
def alias_list_project(db: Session = Depends(get_db)):
    return list_project(db)
