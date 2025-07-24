import pathlib
import os
import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

# ✅ Database y modelos
from app.database import get_db
from app.models import *
from app.models.user import User

# ✅ Routers activos (ya revisados y corregidos)
from app.routes import (
    auth,                # Login, logout, autenticación
    user,                # CRUD usuarios
    project,             # CRUD proyectos
    equipment,           # CRUD equipos
    test_performed,      # Dashboard y mis pruebas
    location,            # Dropdown dinámico
    equipment_type,      # Dropdown dinámico
    test_project         # Activación/desactivación de tests por proyecto (NUEVO)
)

app = FastAPI()

# ✅ Session y CORS middleware
app.add_middleware(SessionMiddleware, secret_key="w97k8Zj9B4fD1VmL3zXeT5GqNpHs0YuA")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Directorios base
BASE_DIR = pathlib.Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# ✅ Configuración Jinja2
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ✅ Página raíz: redirección según rol
@app.get("/", response_class=HTMLResponse)
async def render_index(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=302)

    if user.role == "project":
        return RedirectResponse(url="/admin", status_code=302)

    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Página para usuarios con rol "project"
@app.get("/admin", response_class=HTMLResponse)
async def render_admin(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = db.query(User).filter_by(id=user_id).first()
    if not user or user.role != "project":
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse("index_admin.html", {"request": request})

# ✅ Montar carpeta estática (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ✅ Incluir routers activos
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(project.router)
app.include_router(equipment.router)
app.include_router(test_performed.router)
app.include_router(location.router)
app.include_router(equipment_type.router)
app.include_router(test_project.router)  # ✅ NUEVO, ahora activo

# ✅ Ejecución
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
