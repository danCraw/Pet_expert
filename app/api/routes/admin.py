import sys
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.db.repositories.client import ClientRepository
from app.db.repositories.doctor import DoctorRepository
from app.db.repositories.hospital import HospitalRepository
from app.models.client import ClientOut
from app.models.doctor import DoctorOut
from app.models.hospital import HospitalOut
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


@router.get("/doctors")
@admin
@inject
async def all_doctors(
        token: str,
        doctor_repo: DoctorRepository = Depends(Provide[Container.doctors]),
) -> list[DoctorOut]:
    doctors = await doctor_repo.list()
    return doctors


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
