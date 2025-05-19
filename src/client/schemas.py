from pydantic import BaseModel, UUID4


class ClientIn(BaseModel):
    name: str
    email: str


class ClientOut(BaseModel):
    id: UUID4
    name: str
    email: str
