from fastapi import APIRouter
import subprocess

router = APIRouter()

@router.get("/fix-bcrypt")
def fix_bcrypt():
    try:
        subprocess.run(["pip", "install", "--force-reinstall", "bcrypt==4.1.2"], check=True)
        return {"status": "bcrypt reinstalled successfully"}
    except Exception as e:
        return {"error": str(e)}
