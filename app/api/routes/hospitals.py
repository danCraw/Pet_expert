import sys
from http.client import UNPROCESSABLE_ENTITY
from typing import Any

from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, Depends

from app.db.repositories.hospital import HospitalRepository
from app.db.repositories.review import ReviewRepository
from app.models.auth.base import IdModel
from app.models.auth.hospital import UpdateHospital
from app.models.hospital.base import HospitalCredentials, HospitalIn, HospitalOut, HospitalUpdate
from app.models.review import ReviewOut
from app.redis.tokens import create_access_token

router = APIRouter()


class Container(containers.DeclarativeContainer):
    reviews = providers.Factory(ReviewRepository)

    hospitals = providers.Factory(HospitalRepository)


@router.post("/auth")
@inject
async def auth_hospital(
        credentials: HospitalCredentials,
        hospital_repo: HospitalRepository = Depends(Provide[Container.hospitals]),
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


@router.get("/{hospital_id}")
@inject
async def one_hospital(hospital_id: int,
                       hospital_repo: HospitalRepository = Depends(Provide[Container.hospitals])
                       ) -> HospitalOut:
    hospital = await hospital_repo.get(hospital_id)
    if hospital:
        return hospital
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="hospital with the given Id not found"
    )


@router.post("/")
@inject
async def register_hospital(hospital: HospitalIn,
                            hospital_repo: HospitalRepository = Depends(Provide[Container.hospitals])
                            ) -> dict[str, str | Any]:
    hospital.password_hash = str(hash(hospital.password))
    hospital.password = None
    hospital = await hospital_repo.create(hospital)
    access_token = await create_access_token(hospital)
    return {'access_token': access_token, 'hospital': hospital}


@router.put("/")
@inject
async def update_hospital(hospital: UpdateHospital,
                          hospital_repo: HospitalRepository = Depends(Provide[Container.hospitals])
                          ) -> HospitalOut:
    update_data = hospital.update_data
    if update_data.password:
        update_data.password_hash = str(hash(update_data.password))
        update_data.password = None
    update_data.approved = False
    update_data = await hospital_repo.update(update_data.dict(exclude_none=True))
    if update_data:
        return update_data
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="hospital with the given Id not found"
    )


@router.delete("/{hospital_id}")
@inject
async def delete_hospital(hospital_id,
                          hospital_repo: HospitalRepository = Depends(Provide[Container.hospitals])
                          ) -> list[HospitalOut]:
    hospital = await hospital_repo.delete(hospital_id.id)
    if hospital:
        return hospital
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="hospital with the given Id not found"
    )


@router.get("/reviews/{hospital_id}")
@inject
async def hospital_reviews(
        hospital_id: int,
        review_repo: ReviewRepository = Depends(Provide[Container.reviews]),
        hospital_repo: HospitalRepository = Depends(Provide[Container.hospitals]),
) -> list[ReviewOut]:
    reviews = await hospital_repo.get_reviews(
        hospital_id,
        review_repo,
    )
    if reviews:
        return reviews
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="hospital with the given Id not found"
    )


container = Container()
container.wire(modules=[sys.modules[__name__]])
