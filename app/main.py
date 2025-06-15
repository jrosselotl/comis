from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# ✅ Instancia de FastAPI primero
app = FastAPI()

# ✅ Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Recomendable restringir luego a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Importa y registra rutas
from app.routes import (
    auth,
    usuarios,
    proyectos,
    equipos,
    tests,
    continuidad,
    megado,
    test_pdf
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(proyectos.router)
app.include_router(equipos.router)
app.include_router(tests.router)
app.include_router(continuidad.router)
app.include_router(megado.router)
app.include_router(test_pdf.router)

# ✅ Montar archivos estáticos (como index.html)
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(os.path.dirname(current_dir), "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
