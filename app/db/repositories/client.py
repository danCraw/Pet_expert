from typing import Type

import sqlalchemy
from app.db.tables.clients import Client

from app.db.repositories.base import BaseRepository
from app.models.client import ClientOut, ClientIn


class ClientRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _table(self) -> sqlalchemy.Table:
        return Client

    @property
    def _schema_out(self) -> Type[ClientOut]:
        return ClientOut

    @property
    def _schema_in(self) -> Type[ClientIn]:
        return ClientIn
