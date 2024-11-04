from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schema


def user_get(*, db: Session, user_id: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def users_get(*, db: Session) -> List[models.User]:
    return db.query(models.User).all()


def user_post(*, db: Session, user: schema.UserCreate) -> models.User:
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def user_put(*, db: Session, user_id: str, user: schema.UserCreate) -> Optional[models.User]:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in user.model_dump().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def user_delete(*, db: Session, user_id: str) -> Optional[models.User]:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def user_key_get(*, db: Session, user_id: str, key_id: str) -> Optional[models.ApiKey]:
    return db.query(models.ApiKey).filter(models.ApiKey.user_id == user_id, models.ApiKey.id == key_id).first()


def user_keys_get(*, db: Session, user_id: str) -> List[models.ApiKey]:
    return db.query(models.ApiKey).filter(models.ApiKey.user_id == user_id).order_by(models.ApiKey.last_used_at.desc()).all()


def user_key_post(*, db: Session, key: schema.ApiKeyCreate, user_id: str) -> models.ApiKey:
    db_key = models.ApiKey(**key.model_dump(), user_id=user_id)
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return db_key


def user_key_delete(*, db: Session, key_id: str) -> Optional[models.ApiKey]:
    db_key = db.query(models.ApiKey).filter(models.ApiKey.id == key_id).first()
    if db_key:
        db.delete(db_key)
        db.commit()
    return db_key


def user_request_get(*, db: Session, request_id: str) -> Optional[models.UserRequest]:
    return db.query(models.UserRequest).filter(models.UserRequest.id == request_id).first()


def user_requests_get(*, db: Session, user_id: str, key_id: str) -> List[models.UserRequest]:
    return (
        db.query(models.UserRequest)
            .join(models.ApiKey)
            .filter(models.ApiKey.user_id == user_id, models.ApiKey.id == key_id)
            .all()
    )


def user_request_delete(*, db: Session, request_id: str) -> Optional[models.UserRequest]:
    db_request = db.query(models.UserRequest).filter(models.UserRequest.id == request_id).first()
    if db_request:
        db.delete(db_request)
        db.commit()
    return db_request

