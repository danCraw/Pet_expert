from datetime import datetime
from typing import Optional

from app.models.base import BaseSchema


class AddressBase(BaseSchema):
    diagnosis: str
    dignity: str
    flaws: str
    photos: list[str]
    date_of_receipt: datetime
    phone: str
    pet_name: str
    pet_age: str
    pet_breed: str
    pet_type: str


class AddressIn(AddressBase):
    address_id: Optional[int]


class AddressOut(AddressBase):
    address_id: int
