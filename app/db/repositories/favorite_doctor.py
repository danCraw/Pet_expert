import sqlalchemy

from app.db.repositories.base import BaseRepository
from app.db.tables.favorite_doctor import FavoriteDoctors
from app.models.favorite_doctor import FavouriteDoctor


class FavoriteDoctorsRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def table(self) -> sqlalchemy.Table:
        return FavoriteDoctors

    @property
    def _schema_in(self):
        return FavouriteDoctor

    @property
    def _schema_out(self):
        return FavouriteDoctor
