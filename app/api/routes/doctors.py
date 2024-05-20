import sys
from http.client import UNPROCESSABLE_ENTITY
from typing import Dict, Any

from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, Depends

from app.db.repositories.doctor import DoctorRepository
from app.models.auth.doctor import UpdateDoctor
from app.models.doctor.base import DoctorIn, DoctorCredentials
from app.models.doctor.base import DoctorOut
from app.models.doctor.filters import DoctorFilterModel
from app.models.review import ReviewOut
from app.redis.tokens import create_access_token
from app.redis.doctors.auth import doctor

router = APIRouter()


class Container(containers.DeclarativeContainer):
    doctors = providers.Factory(DoctorRepository)


@router.post("/auth")
@inject
async def auth_doctor(
        credentials: DoctorCredentials,
        hospital_repo: DoctorRepository = Depends(Provide[Container.doctors]),
) -> dict[str, str | Any]:
    client = await hospital_repo.get_by_credentials(
        credentials.email,
        str(hash(credentials.password)),
    )
    if client:
        access_token = await create_access_token(client)
        return {'access_token': access_token, 'client': client}
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="hospital with the given params not found"
    )


@router.get("/{doctor_id}")
@inject
async def one_doctor(
        doctor_id: int,
        doctor_repo: DoctorRepository = Depends(Provide[Container.doctors])
) -> DoctorOut:
    doctor = await doctor_repo.get(doctor_id)
    if doctor:
        return doctor
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="doctor with the given Id not found"
    )


@router.get("/doctors")
@inject
async def all_doctors(
        filters: DoctorFilterModel,
        doctor_repo: DoctorRepository = Depends(Provide[Container.doctors]),
) -> list[DoctorOut]:
    doctors = await doctor_repo.filtered_list(filters)
    return doctors


@router.post("/")
@inject
async def register_doctor(
        doctor: DoctorIn,
        doctor_repo: DoctorRepository = Depends(Provide[Container.doctors])
) -> dict[str, str | Any]:
    doctor.password_hash = str(hash(doctor.password))
    doctor.password = None
    doctor = await doctor_repo.create(doctor)
    access_token = await create_access_token(doctor)
    return {'access_token': access_token, 'doctor': doctor}


@router.put("/")
@doctor
@inject
async def update_doctor(
        doctor: UpdateDoctor,
        doctor_repo: DoctorRepository = Depends(Provide[Container.doctors])
) -> DoctorOut:
    update_data = doctor.update_data
    if update_data.password:
        update_data.password_hash = str(hash(update_data.password))
        update_data.password = None
    update_data.approved = False
    update_data = await doctor_repo.update(update_data)
    if update_data:
        return update_data
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="doctor with the given Id not found"
    )


@router.get("/reviews/{doctor_id}")
@inject
async def doctor_reviews(
        doctor_id: int,
        doctor_repo: DoctorRepository = Depends(Provide[Container.doctors]),
) -> list[ReviewOut]:
    reviews = await doctor_repo.get_reviews(
        doctor_id,
    )
    if reviews:
        return reviews
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="doctor with the given Id not found"
    )


container = Container()
container.wire(modules=[sys.modules[__name__]])
