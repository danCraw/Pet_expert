import sys
from http.client import UNPROCESSABLE_ENTITY

from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, Depends

from app.db.repositories.doctor import DoctorRepository
from app.db.repositories.review import ReviewRepository
from app.models.doctor import DoctorIn
from app.models.doctor import DoctorOut
from app.models.review import ReviewOut

router = APIRouter()


class Container(containers.DeclarativeContainer):

    doctors = providers.Factory(DoctorRepository)

    reviews = providers.Factory(ReviewRepository)


@router.get("/")
@inject
async def doctors_list(doctor_repo: DoctorRepository = Depends(Provide[Container.doctors])) -> list[DoctorOut]:
    doctor = await doctor_repo.list()
    return doctor


@router.get("/{doctor_id}")
@inject
async def one_doctor(doctor_id: int, doctor_repo: DoctorRepository = Depends(
                           Provide[Container.doctors])) -> DoctorOut:
    doctor = await doctor_repo.get(doctor_id)
    if doctor:
        return doctor
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="doctor with the given Id not found")


@router.post("/")
@inject
async def create_doctor(doctor: DoctorIn, doctor_repo: DoctorRepository = Depends(
                              Provide[Container.doctors])) -> DoctorOut:
    doctor.password_hash = str(hash(doctor.password))
    doctor.password = None
    doctor = await doctor_repo.create(doctor)
    return doctor


@router.put("/")
@inject
async def update_doctor(doctor: DoctorIn, doctor_repo: DoctorRepository = Depends(
                              Provide[Container.doctors])) -> DoctorOut:
    doctor.approved = False
    doctor = await doctor_repo.update(doctor)
    if doctor:
        return doctor
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="doctor with the given Id not found")


@router.delete("/{doctor_id}")
@inject
async def delete_doctor(doctor_id: int, doctor_repo: DoctorRepository = Depends(
                              Provide[Container.doctors])) -> list[DoctorOut]:
    doctor = await doctor_repo.delete(doctor_id)
    if doctor:
        return doctor
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="doctor with the given Id not found")


@router.get("reviews/{doctor_id}")
@inject
async def doctor_reviews(doctor_id: int, doctor_repo: DoctorRepository = Depends(Provide[Container.doctors]),
    review_repo: ReviewRepository = Depends(Provide[Container.reviews])) -> list[ReviewOut]:
    reviews = await review_repo.get_doctor_reviews(doctor_id, doctor_repo)
    if reviews:
        return reviews
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="doctor with the given Id not found")

container = Container()
container.wire(modules=[sys.modules[__name__]])

