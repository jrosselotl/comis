from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="una_clave_segura_123")
# ✅ Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Importar y registrar rutas
from app.routes import (
    auth,
    usuarios,
    proyectos,
    equipos,
    tests,
    continuidad,
    megado,
    test_pdf,
    formulario  # si ya tienes el formulario.py
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(proyectos.router)
app.include_router(equipos.router)
app.include_router(tests.router)
app.include_router(continuidad.router)
app.include_router(megado.router)
app.include_router(test_pdf.router)
app.include_router(formulario.router)

# ✅ Directorio de plantillas
templates = Jinja2Templates(directory="app/templates")

# ✅ Ruta principal para renderizar index.html desde templates
@app.get("/", response_class=HTMLResponse)
async def render_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Montar carpeta estática (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
from app.routes import formulario
app.include_router(formulario.router)
