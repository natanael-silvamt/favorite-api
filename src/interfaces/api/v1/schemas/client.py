from pydantic import BaseModel, EmailStr
from uuid import UUID
from core.entities.client import Client


class ClientIn(BaseModel):
    name: str
    email: EmailStr


class ClientOut(BaseModel):
    id: UUID
    name: str
    email: str
