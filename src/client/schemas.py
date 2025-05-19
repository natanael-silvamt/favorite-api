from pydantic import UUID4, BaseModel


class ClientIn(BaseModel):
    name: str
    email: str


class ClientOut(BaseModel):
    id: UUID4
    name: str
    email: str
