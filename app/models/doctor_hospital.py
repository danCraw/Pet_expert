from datetime import datetime

from app.models.base import BaseSchema


class DoctorHospitalBase(BaseSchema):
    doctor_id: int
    hospital_id: int
    start_date: datetime
    end_date: datetime


class DoctorHospitalIn(DoctorHospitalBase):
    doctor_id: int
    hospital_id: int


class DoctorHospitalOut(DoctorHospitalBase):
    doctor_id: int
    hospital_id: int

