import os
import pathlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

# Crear app
app = FastAPI()

# Middleware de sesión y CORS
app.add_middleware(SessionMiddleware, secret_key="una_clave_segura_123")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar rutas
from app.routes import (
    auth, usuarios, proyectos, equipos, tests,
    continuidad, megado, test_pdf, formulario
)

# Registrar rutas
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(proyectos.router)
app.include_router(equipos.router)
app.include_router(tests.router)
app.include_router(continuidad.router)
app.include_router(megado.router)
app.include_router(test_pdf.router)
app.include_router(formulario.router)

# Rutas absolutas a static/ y templates/
BASE_DIR = pathlib.Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"

# Templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/", response_class=HTMLResponse)
async def render_index(request: Request):
    if not request.session.get("usuario_id"):
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("index.html", {"request": request})

# Static
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
