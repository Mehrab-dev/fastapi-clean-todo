from sqlalchemy import String, DateTime, ForeignKey, Boolean, UUID as uuid, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from uuid import UUID, uuid4
from datetime import datetime, timezone

from app.infrastructure.database.base import  Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(uuid, primary_key=True, default=uuid4, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    """ relationships """
    profile = relationship("ProfileModel", back_populates="user", cascade="all, delete-orphan", uselist=False)
    tasks = relationship("TaskModel", back_populates="user", cascade="all, delete-orphan")




class ProfileModel(Base):
    __tablename__ = "profiles"

    id: Mapped[UUID] = mapped_column(uuid, primary_key=True, nullable=False, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(uuid, ForeignKey("users.id"), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    image: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    """ relationships """
    user = relationship("UserModel", back_populates="profile", uselist=False)




class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(uuid, primary_key=True, default=uuid4, nullable=False)
    user_id: Mapped[UUID] = mapped_column(uuid, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    """ relationship """
    user = relationship("UserModel", back_populates="tasks")