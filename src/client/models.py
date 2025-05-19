import uuid
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class Client(SQLModel, table=True):
    __tablename__ = 'clients'
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
