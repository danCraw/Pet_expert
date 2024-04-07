from app.models.auth.base import Token
from app.models.hospital.base import HospitalUpdate


class UpdateHospital(Token):
    update_data: HospitalUpdate
