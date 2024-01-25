import sqlalchemy
from asyncpg import Record

from app.db.repositories.base import BaseRepository
from app.db.tables.reply import Reply
from app.models.reply import ReplyIn, ReplyOut


class ReplyRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def table(self) -> sqlalchemy.Table:
        return Reply

    @property
    def _schema_out(self) -> type[ReplyOut]:
        return ReplyOut

    @property
    def _schema_in(self) -> type[ReplyIn]:
        return ReplyIn

    async def _list(self, review_id: int) -> list[Record]:
        query = self.table.select().where(self.table.c.review_id == review_id)
        return await self._db.fetch_all(query=query)

    async def list(self, review_id: int) -> list:
        rows = await self._list(review_id)
        return [self._schema_out(**dict(row)) for row in rows]
