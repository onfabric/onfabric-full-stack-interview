from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/health")
async def health_check():
    return "ok"


@router.get("/health/db")
async def db_health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
