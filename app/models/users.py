from sqlalchemy import DateTime,func,TEXT,Boolean,CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from  sqlalchemy.orm import Mapped,mapped_column
import uuid

from db.base import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        TEXT,
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        TEXT,
        unique=True,
        nullable=False
    )
    sign_up_type: Mapped[str] = mapped_column(
        TEXT,
        nullable=False
    )
    password: Mapped[str] = mapped_column(
        TEXT,
        nullable=True,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    __table_args__ = (
        CheckConstraint(
            "sign_up_type IN ('app login','google login')",
            name="valid_sign_up_type"
        ),
    )