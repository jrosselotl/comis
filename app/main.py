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

# Base de datos y modelos
from app.database import get_db
from app.models.usuario import Usuario

# Routers principales
from app.routes import (
    auth,
    usuarios,
    proyectos,
    equipos,
    tests,
    continuidad,
    megado,
    formulario,
    contact_resistance,
    torque,
    test_realizados,      # ✅ NUEVO (dashboard y my tests)
    ubicaciones,          # ✅ NUEVO (poblar dropdowns dinámicos)
    tipo_equipos          # ✅ NUEVO (poblar dropdowns dinámicos)
)

app = FastAPI()

# Middleware de sesiones y CORS
app.add_middleware(SessionMiddleware, secret_key="w97k8Zj9B4fD1VmL3zXeT5GqNpHs0YuA")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directorios base
BASE_DIR = pathlib.Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Configuración de Jinja2
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Página raíz: redirige según el rol del usuario
@app.get("/", response_class=HTMLResponse)
async def render_index(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)

    usuario = db.query(Usuario).filter_by(id=usuario_id).first()
    if not usuario:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=302)

    if usuario.rol == "proyecto":
        return RedirectResponse(url="/admin", status_code=302)

    return templates.TemplateResponse("index.html", {"request": request})

# Página para usuarios con rol "proyecto"
@app.get("/admin", response_class=HTMLResponse)
async def render_admin(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)

    usuario = db.query(Usuario).filter_by(id=usuario_id).first()
    if not usuario or usuario.rol != "proyecto":
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse("index_admin.html", {"request": request})

# Montar carpeta /static para CSS/JS
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Incluir todos los routers
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(proyectos.router)
app.include_router(equipos.router)
app.include_router(tests.router)
app.include_router(continuidad.router)
app.include_router(megado.router)
app.include_router(contact_resistance.router)
app.include_router(torque.router)
app.include_router(formulario.router)
app.include_router(test_realizados.router)  # ✅ My Tests y Dashboard
app.include_router(ubicaciones.router)      # ✅ Dropdown ubicaciones dinámicas
app.include_router(tipo_equipos.router)     # ✅ Dropdown equipos dinámicos

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
