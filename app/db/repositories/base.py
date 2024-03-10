import abc
import uuid
from typing import Dict, List, Union

import databases
import sqlalchemy
from asyncpg import Record
from sqlalchemy import column

from app.db.base import database
from app.models.base import BaseIdSchema, BaseSchema


class BaseRepository(abc.ABC):
    def __init__(self,
                 *_,
                 db: databases.Database = database,
                 **__,
                 ) -> None:
        self._db = db
        super()

    @property
    @abc.abstractmethod
    def table(self) -> sqlalchemy.Table:
        pass

    @property
    @abc.abstractmethod
    def _schema_out(self):
        pass

    @property
    @abc.abstractmethod
    def _schema_in(self):
        pass

    @staticmethod
    def generate_uuid() -> uuid.UUID:
        return uuid.uuid4()

    def _preprocess_create(self, values: Dict) -> Dict:
        if values.get(self.table.c[0].description, None) is None:
            values.pop(self.table.c[0].description)  # removing None id
        if values.get('password', None) is None:
            values.pop('password')
        return values

    async def _list(self) -> List[Record]:
        query = self.table.select()
        rows = await self._db.fetch_all(query=query)
        return rows

    async def list(self) -> List:
        rows = await self._list()
        return [self._schema_out(**dict(row)) for row in rows]

    async def create(self, values: Union[BaseSchema, Dict]) -> _schema_out:
        if isinstance(values, dict):
            values = self._schema_in(**values)
        dict_values = dict(values.dict(exclude_none=True))

        query = self.table.insert()
        query = query.values(dict_values)
        query = query.returning(self.table.c[0])

        result = await self._db.execute(query=query)
        dict_values.update({self.table.c[0].description: result})
        return self._schema_out(**dict_values)

    async def get(self, id_: Union[int, str]) -> _schema_out:

        query = self.table.select()
        query = query.where(column(self.table.c[0].description) == id_)

        row = await self._db.fetch_one(query=query)
        if row:
            return self._schema_out(**dict(dict(row).items()))
        return row

    async def update(self, values: Union[BaseIdSchema, Dict]) -> _schema_out:
        if isinstance(values, dict):
            values = self._schema_in(**values)
        dict_values = self._preprocess_create(dict(values))
        row = await self.get(dict_values['id'])
        if row:

            query = self.table.update()
            query = query.where(self.table.c.id == dict_values['id'])

            await self._db.execute(query=query,
                                   values=dict_values)
            return self._schema_out(**dict_values)
        return row

    async def delete(self, id_: Union[int, str]) -> _schema_out:
        row = await self.get(id_)
        if row:

            query = self.table.delete()
            query = query.where(column(self.table.c[0].description) == id_)

            await self._db.execute(query=query)
        return row
