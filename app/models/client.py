from typing import Optional

from app.models.base import BaseSchema


class ClientBase(BaseSchema):
    name: str
    surname: str
    patronomic: str
    photo: str
    phone: str
    email: str
    password: Optional[str]


class ClientIn(ClientBase, extra='allow'):
    id: Optional[int]


class ClientOut(ClientBase):
    id: int

    class Config:
        fields = {
            'some_flag': {
                'exclude': {'password'}
            }
        }
