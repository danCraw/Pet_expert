import sqlalchemy

from app.db.repositories.base import BaseRepository
from app.db.tables.favorite_hospital import favorite_hospitals
from app.models.favorite_hospital import FavouriteHospital


class FavouriteHospitalsRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def table(self) -> sqlalchemy.Table:
        return favorite_hospitals

    @property
    def _schema_in(self):
        return FavouriteHospital

    @property
    def _schema_out(self):
        return FavouriteHospital
