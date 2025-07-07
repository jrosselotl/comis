from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
import os
import uvicorn

# Importar base de datos y modelos
from app.database import get_db
from app.models.usuario import Usuario
from app.routes.auth import router as auth_router
from app.routes.formulario import router as formulario_router


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


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
