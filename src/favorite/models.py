import uuid
from sqlmodel import Field, SQLModel


class Favorite(SQLModel, table=True):
    __tablename__ = 'favorites'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    client_id: uuid.UUID = Field(default=None, foreign_key="clients.id")
    product_id: int = Field(default=None)
