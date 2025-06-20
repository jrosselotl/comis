from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from passlib.hash import bcrypt
from passlib.context import CryptContext

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/auth/login")
def login(
    request: Request,
    correo: str = Form(...),
    password: str = Form(...),
    recordar: bool = Form(False),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter_by(correo=correo).first()
    if not usuario or not pwd_context.verify(password, usuario.password_hash):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciales inválidas"})

    request.session["usuario_id"] = usuario.id
    if recordar:
        request.session["recordar"] = True
    return RedirectResponse(url="/", status_code=HTTP_302_FOUND)

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)
