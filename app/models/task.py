from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from app.core.database import Base
from datetime import datetime


from typing import TYPE_CHECKING

from app.schemas.enum import TaskStatus
if TYPE_CHECKING:
    from app.models.user import User

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(String(50), nullable=False, default=TaskStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="tasks")