from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime

class RolUsuario(str, Enum):
    admin = "admin"
    tecnico = "tecnico"

# Para crear nuevos usuarios
class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr
    password: str  # solo en creación

# Para mostrar datos del usuario
class UsuarioOut(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    rol: RolUsuario
    fecha_registro: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)  # Pydantic v2 ✅

# Para login
class UsuarioLogin(BaseModel):
    correo: EmailStr
    password: str
