from sqlalchemy import Integer, String, Text, Boolean, DateTime, ForeignKey, UUID as uuid
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from uuid import UUID
from datetime import date, datetime, timezone

from app.infrastructure.database.base import Base


__all__ = ["UserModel", "ProfileModel", "TaskModel"]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(uuid, primary_key=True, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[date] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[date] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    """ relationships """
    profile = relationship("ProfileModel", back_populates="user")
    tasks = relationship("TaskModel", back_populates="user")



class ProfileModel(Base):
    __tablename__ = "profiles"

    id: Mapped[UUID] = mapped_column(uuid, primary_key=True, unique=True, nullable=False)
    user_id: Mapped[UUID] = mapped_column(uuid, ForeignKey("users.id"), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    image: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[date] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[date] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    """ relationships """
    user = relationship("UserModel", back_populates="profile", uselist=False)



class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(uuid, primary_key=True, nullable=False, unique=True)
    user_id: Mapped[UUID] = mapped_column(uuid, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[date] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[date] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    """ relationships """
    user = relationship("UserModel", back_populates="tasks")