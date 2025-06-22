from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.models.usuario import Usuario
from app.database import get_db
from passlib.context import CryptContext
from fastapi import Form

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crear nuevo usuario
@router.post("/", response_model=UsuarioOut)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    hashed_pw = pwd_context.hash(usuario.password)
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        password_hash=hashed_pw
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# Obtener todos los usuarios
@router.get("/", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.post("/reset-password")
def reset_password(
    correo: str = Form(...),
    nueva_password: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter_by(correo=correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.password_hash = pwd_context.hash(nueva_password)
    db.commit()
    return {"mensaje": "Contraseña actualizada correctamente"}
