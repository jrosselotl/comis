import pathlib
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Middleware de sesiones y CORS
app.add_middleware(SessionMiddleware, secret_key="una_clave_segura_123")
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

# Página raíz: redirige según el rol guardado en sesión
@app.get("/", response_class=HTMLResponse)
async def render_index(request: Request):
    if not request.session.get("usuario_id") or not request.session.get("usuario_rol"):
        return RedirectResponse(url="/login", status_code=302)

    if request.session["usuario_rol"] == "proyecto":
        return RedirectResponse(url="/admin", status_code=302)

    return templates.TemplateResponse("index.html", {"request": request})

# Página para usuarios con rol "proyecto"
@app.get("/admin", response_class=HTMLResponse)
async def render_admin(request: Request):
    if not request.session.get("usuario_id") or request.session.get("usuario_rol") != "proyecto":
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("index_admin.html", {"request": request})

# Montar carpeta /static para CSS/JS
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Incluir rutas
from app.routes import (
    auth, usuarios, proyectos, equipos, tests,
    continuidad, megado, test_pdf, formulario
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
