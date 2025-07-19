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

# Database and models
from app.database import get_db
from app.models.usuario import Usuario

# Main routers
from app.routes import (
    auth,
    user,
    project,
    equipment,
    test,
    continuity,
    isolation,
    contact_resistance,
    torque,
    test_performed,     # ✅ Dashboard and My Tests
    location,           # ✅ Dynamic dropdowns for locations
    equipment_type      # ✅ Dynamic dropdowns for equipment
)

app = FastAPI()

# Session and CORS middleware
app.add_middleware(SessionMiddleware, secret_key="w97k8Zj9B4fD1VmL3zXeT5GqNpHs0YuA")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directories
BASE_DIR = pathlib.Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Jinja2 configuration
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Root page: redirect based on user role
@app.get("/", response_class=HTMLResponse)
async def render_index(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = db.query(Usuario).filter_by(id=user_id).first()
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=302)

    if user.rol == "project":
        return RedirectResponse(url="/admin", status_code=302)

    return templates.TemplateResponse("index.html", {"request": request})

# Page for users with "project" role
@app.get("/admin", response_class=HTMLResponse)
async def render_admin(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = db.query(Usuario).filter_by(id=user_id).first()
    if not user or user.rol != "project":
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse("index_admin.html", {"request": request})

# Mount /static folder for CSS/JS
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Include all routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(project.router)
app.include_router(equipment.router)
app.include_router(test.router)
app.include_router(continuity.router)
app.include_router(isolation.router)
app.include_router(contact_resistance.router)
app.include_router(torque.router)
app.include_router(test_performed.router)  # ✅ My Tests and Dashboard
app.include_router(location.router)        # ✅ Dynamic location dropdowns
app.include_router(equipment_type.router)  # ✅ Dynamic equipment dropdowns

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
