from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Response(BaseModel):
    content: Any
    status_code: int


class Config(BaseModel):
    max_connections: int = Field(default=100)
    retry_attempts: int = Field(default=1)


class Method(str, Enum):
    get = 'get'
