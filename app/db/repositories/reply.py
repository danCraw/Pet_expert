import sqlalchemy

from app.db.repositories.base import BaseRepository
from app.db.tables.reply import Reply
from app.models.review import ReviewOut, ReviewIn


class ReplyRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def table(self) -> sqlalchemy.Table:
        return Reply

    @property
    def _schema_out(self) -> type[ReviewOut]:
        return ReviewOut

    @property
    def _schema_in(self) -> type[ReviewIn]:
        return ReviewIn

