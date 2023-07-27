import sqlalchemy

from app.db.repositories.base import BaseRepository
from app.db.tables.favorite_hospital import FavoriteHospitals


class FavoriteHospitalsRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _table(self) -> sqlalchemy.Table:
        return FavoriteHospitals
