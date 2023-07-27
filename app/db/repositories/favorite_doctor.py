import sqlalchemy

from app.db.repositories.base import BaseRepository
from app.db.tables.favorite_doctor import FavoriteDoctors


class FavoriteDoctorsRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _table(self) -> sqlalchemy.Table:
        return FavoriteDoctors
