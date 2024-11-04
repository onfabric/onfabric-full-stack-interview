from typing import Generator, Optional
from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.db import SessionLocal
from app import models



def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_from_key(
    x_api_key: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> models.User:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
        
    key = db.query(models.ApiKey).filter(models.ApiKey.key == x_api_key).first()
    if not key:
        raise HTTPException(status_code=401, detail="Invalid API key")
        
    user = db.query(models.User).filter(models.User.id == key.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    key.last_used_at = datetime.now()
    db.commit()

    return user
