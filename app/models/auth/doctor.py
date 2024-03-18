from app.models.auth.base import Token
from app.models.doctor.base import DoctorUpdate


class UpdateDoctor(Token):
    update_data: DoctorUpdate

