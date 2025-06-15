from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    auth,
    usuarios,
    proyectos,
    equipos,
    tests,
    continuidad,
    megado,
    test_pdf,  # tu nueva ruta de prueba
)
from fastapi.staticfiles import StaticFiles
import os

# Calcula la ruta absoluta de /static dentro de /app
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(os.path.dirname(current_dir), "static")

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
#from app.routes.enviar_pdf import router as pdf_router
#app.include_router(pdf_router)
# ✅ Instancia FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"mensaje": "FastAPI funcionando en cPanel con Passenger"}
# ✅ Middleware CORS (opcional, pero recomendable)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir a tu dominio si prefieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Rutas registradas
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(proyectos.router)
app.include_router(equipos.router)
app.include_router(tests.router)
app.include_router(continuidad.router)
app.include_router(megado.router)
app.include_router(test_pdf.router)

