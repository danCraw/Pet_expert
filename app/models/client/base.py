from typing import Optional

from pydantic import BaseModel

from app.models.base import BaseSchema, BaseCredentials


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


class ClientUpdate(BaseModel):
    id: Optional[int]
    name: Optional[str]
    surname: Optional[str]
    patronomic: Optional[str]
    photo: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    password: Optional[str]
    password_hash: Optional[str]


class ClientCredentials(BaseCredentials):
    pass
