import sqlalchemy

from app.db.repositories.base import BaseRepository
from app.db.tables.favorite_doctor import favorite_doctors
from app.models.favorite_doctor import FavouriteDoctor


class FavoriteDoctorsRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def table(self) -> sqlalchemy.Table:
        return favorite_doctors

    @property
    def _schema_in(self):
        return FavouriteDoctor

    @property
    def _schema_out(self):
        return FavouriteDoctor
