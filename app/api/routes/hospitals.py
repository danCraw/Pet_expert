import sys
from http.client import UNPROCESSABLE_ENTITY

from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, Depends

from app.db.repositories.hospital import HospitalRepository
from app.models.hospital import HospitalIn
from app.models.hospital import HospitalOut

router = APIRouter()


class Container(containers.DeclarativeContainer):

    hospitals = providers.Factory(HospitalRepository)


@router.get("/")
@inject
async def hospitals_list(hospital_repo: HospitalRepository = Depends(Provide[Container.hospitals])) -> list[HospitalOut]:
    hospital = await hospital_repo.list()
    return hospital


@router.get("/{hospital_id}")
@inject
async def one_hospital(hospital_id: int, hospital_repo: HospitalRepository = Depends(
                           Provide[Container.hospitals])) -> HospitalOut:
    hospital = await hospital_repo.get(hospital_id)
    if hospital:
        return hospital
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="hospital with the given Id not found")


@router.post("/")
@inject
async def create_hospital(hospital: HospitalIn, hospital_repo: HospitalRepository = Depends(
                              Provide[Container.hospitals])) -> HospitalOut:
    hospital = await hospital_repo.create(hospital)
    return hospital


@router.put("/")
@inject
async def update_hospital(hospital: HospitalIn, hospital_repo: HospitalRepository = Depends(
                              Provide[Container.hospitals])) -> HospitalOut:
    hospital.approved = False
    hospital = await hospital_repo.update(hospital)
    if hospital:
        return hospital
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="hospital with the given Id not found")


@router.delete("/{hospital_id}")
@inject
async def delete_hospital(hospital_id: int, hospital_repo: HospitalRepository = Depends(
                              Provide[Container.hospitals])) -> list[HospitalOut]:
    hospital = await hospital_repo.delete(hospital_id)
    if hospital:
        return hospital
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="hospital with the given Id not found")


container = Container()
container.wire(modules=[sys.modules[__name__]])
