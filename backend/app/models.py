from app.core.db import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated, Optional
from datetime import datetime


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )


class User(TimestampMixin, Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    email: Mapped[str] = mapped_column(index=True)
    fullname: Mapped[Optional[str]] = mapped_column(String(30))
    nickname: Mapped[Optional[str]]

    keys: Mapped[list["ApiKey"]] = relationship("ApiKey", back_populates="user")


class ApiKey(TimestampMixin, Base):
    __tablename__ = "user_keys"
    id: Mapped[str] = mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
    key: Mapped[str] = mapped_column(String(64), unique=True, index=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = mapped_column(String(30))
    last_used_at: Mapped[Optional[datetime]] = mapped_column(nullable=True, server_default=text("CURRENT_TIMESTAMP"))

    user: Mapped["User"] = relationship("User", back_populates="keys")


class UserRequest(TimestampMixin, Base):
    __tablename__ = "user_requests"
    id: Mapped[str] = mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    key_id: Mapped[str] = mapped_column(ForeignKey("user_keys.id"), index=True)
    endpoint: Mapped[str] = mapped_column(String(256))
    method: Mapped[str] = mapped_column(String(10))
    status_code: Mapped[int]

    key: Mapped["ApiKey"] = relationship("ApiKey")



