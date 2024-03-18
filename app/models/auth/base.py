from pydantic import BaseModel

from app.models.client.base import ClientUpdate
from app.models.favorite_doctor import FavouriteDoctor
from app.models.favorite_hospital import FavouriteHospital


class Token(BaseModel):
    token: str


class IdModel(Token):
    id: int
