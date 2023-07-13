from typing import Optional

from app.models.base import BaseSchema


class ClientBase(BaseSchema):
    name: str
    surname: str
    patronomic: str
    photo: str
    email: str
    password_hash: str


class ClientIn(ClientBase):
    client_id: Optional[int]


class ClientOut(ClientBase):
    client_id: int

