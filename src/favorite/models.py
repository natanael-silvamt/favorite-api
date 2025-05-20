import uuid
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import Field, SQLModel


class Favorite(SQLModel, table=True):
    __tablename__ = 'favorites'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc),
        },
        sa_type=TIMESTAMP(timezone=True),
    )
    client_id: uuid.UUID = Field(default=None, foreign_key="clients.id")
    product_id: int = Field(default=None)
