import uuid
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import Field, SQLModel


class Client(SQLModel, table=True):
    __tablename__ = 'clients'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc),
        },
        sa_type=TIMESTAMP(timezone=True),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc),
        },
        sa_type=TIMESTAMP(timezone=True),
    )
    deleted_at: datetime | None = Field(
        default=None,
        nullable=True,
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc),
        },
        sa_type=TIMESTAMP(timezone=True),
    )
    name: str = Field(max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
