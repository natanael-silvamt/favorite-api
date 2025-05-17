from uuid import UUID

from pydantic import BaseModel


class Client(BaseModel):
    id: UUID
    name: str
    email: str
