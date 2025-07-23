from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Models
from app.database import get_db
from app.models.user import User
from app.models.test_continuity import TestContinuity
from app.models.test_isolation import TestIsolation
from app.models.test_contact_resistance import TestContactResistance
from app.models.test_torque import TestTorque

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Login page
@router.get("/login", response_class=HTMLResponse)
def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# ✅ Process login
@router.post("/auth/login")
def process_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember: bool = Form(False),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(email=email).first()

    if not user or not pwd_context.verify(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"}
        )

    # ✅ Save session data
    request.session["user_id"] = user.id
    request.session["user_role"] = user.role
    if remember:
        request.session["remember"] = True

    # ✅ Redirect based on role
    if user.role == "project":
        return RedirectResponse(url="/admin", status_code=HTTP_302_FOUND)
    else:
        return RedirectResponse(url="/", status_code=HTTP_302_FOUND)

# ✅ Logout
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)

# ✅ Get current user (IMPORTANTE PARA GUARDAR USER_ID)
def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
