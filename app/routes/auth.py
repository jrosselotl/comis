from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.test_continuidad import TestContinuidad
from app.models.test_megado import TestMegado

from app.database import get_db
from app.models.usuario import Usuario

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Página de login
@router.get("/login", response_class=HTMLResponse)
def mostrar_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Procesar login
@router.post("/auth/login")
def procesar_login(
    request: Request,
    correo: str = Form(...),
    password: str = Form(...),
    recordar: bool = Form(False),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter_by(correo=correo).first()

    if not usuario or not pwd_context.verify(password, usuario.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Credenciales inválidas"}
        )

    # Guardar datos en sesión
    request.session["usuario_id"] = usuario.id
    request.session["usuario_rol"] = usuario.rol
    if recordar:
        request.session["recordar"] = True

    # Redirigir según el rol
    if usuario.rol == "proyecto":
        return RedirectResponse(url="/admin", status_code=HTTP_302_FOUND)
    else:
        return RedirectResponse(url="/", status_code=HTTP_302_FOUND)

# Cerrar sesión
@router.get("/logout")
def cerrar_sesion(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)
