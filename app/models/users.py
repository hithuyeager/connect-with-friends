from sqlalchemy import (
    DateTime,func,TEXT,Boolean,
    CheckConstraint,BigInteger,
    ForeignKey,text
    )
from sqlalchemy.dialects.postgresql import UUID
from  sqlalchemy.orm import Mapped,mapped_column
import uuid

from db.base import Base
from datetime import datetime

class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
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
    google_sub: Mapped[str] = mapped_column(
        TEXT,
        nullable=True,
        unique=True
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=True
    )
    __table_args__ = (
        CheckConstraint(
            "sign_up_type IN ('app login','google login')",
            name="valid_sign_up_type"
        ),
    )

class Sessions(Base):

    __tablename__ = "sessions"
    
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id",ondelete="CASCADE"),
        nullable=False
    )
    hashed_refresh_token: Mapped[str] = mapped_column(
        TEXT,
        nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class Messages(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    room_id: Mapped[str] = mapped_column(
        TEXT,
        nullable=False 
    )

    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        TEXT,
        nullable=True
    )

    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

