from datetime import datetime
from typing import Optional
from enum import Enum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import func, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class RoleName(Enum):
    admin: str = "admin"
    staff: str = "staff"
    customer: str = "customer"


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[RoleName] = mapped_column(
        SQLEnum(RoleName), nullable=False, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return str(self.name.name)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False
    )

    role: Mapped["Role"] = relationship(back_populates="users")

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def __str__(self) -> str:
        return self.username
