from pydantic import UUID4, BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    hashed_password: str
    is_superuser: bool = False


class UserIn(UserBase):
    pass


class UserOut(UserBase):
    id: UUID4
