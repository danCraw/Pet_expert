import sys
from http.client import UNPROCESSABLE_ENTITY

from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from app.db.repositories.client import ClientRepository
from app.db.repositories.doctor import DoctorRepository
from app.db.repositories.hospital import HospitalRepository
from app.models.auth.base import IdModel
from app.models.client.base import ClientOut
from app.models.doctor.base import DoctorOut
from app.models.hospital.base import HospitalOut
from app.redis.admins.auth import admin

router = APIRouter()


class Container(containers.DeclarativeContainer):
    clients = providers.Factory(ClientRepository)

    doctors = providers.Factory(DoctorRepository)

    hospitals = providers.Factory(HospitalRepository)


@router.get("/clients")
@admin
@inject
async def all_clients(
        token: str,
        client_repo: ClientRepository = Depends(Provide[Container.clients]),
) -> list[ClientOut]:
    clients = await client_repo.list()
    return clients


@router.delete("/doctors/{doctor_id}")
@admin
@inject
async def delete_doctor(
        doctor: IdModel,
        doctor_repo: DoctorRepository = Depends(Provide[Container.doctors])
) -> list[DoctorOut]:
    doctor = await doctor_repo.delete(doctor.id)
    if doctor:
        return doctor
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="doctor with the given Id not found"
    )


@router.get("/hospitals")
@admin
@inject
async def all_hospitals(
        token: str,
        hospital_repo: HospitalRepository = Depends(Provide[Container.hospitals]),
) -> list[HospitalOut]:
    hospital = await hospital_repo.list()
    return hospital

container = Container()
container.wire(modules=[sys.modules[__name__]])
