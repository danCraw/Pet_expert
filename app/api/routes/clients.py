import sys
from http.client import UNPROCESSABLE_ENTITY
from typing import Any

from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, Depends

from app.db.repositories.client import ClientRepository
from app.db.repositories.doctor import DoctorRepository
from app.db.repositories.favorite_doctor import FavoriteDoctorsRepository
from app.db.repositories.favourite_hospital import FavouriteHospitalsRepository
from app.db.repositories.hospital import HospitalRepository
from app.db.repositories.review import ReviewRepository
from app.db.repositories.visit import VisitRepository
from app.models.auth.base import IdModel
from app.models.auth.client import UpdateClient, AddHospitalToFavouriteClient, FavouriteDoctorClient
from app.models.client.base import ClientIn, ClientOut, ClientCredentials
from app.models.doctor.base import DoctorOut
from app.models.favorite_hospital import FavouriteHospital
from app.models.hospital.base import HospitalOut
from app.models.review import ReviewOut
from app.redis.clients.auth import client
from app.redis.tokens import create_access_token

router = APIRouter()


class Container(containers.DeclarativeContainer):
    clients = providers.Factory(ClientRepository)

    doctors = providers.Factory(DoctorRepository)

    hospitals = providers.Factory(HospitalRepository)

    favorite_doctors = providers.Factory(FavoriteDoctorsRepository)

    favourite_hospitals = providers.Factory(FavouriteHospitalsRepository)

    visits = providers.Factory(VisitRepository)

    reviews = providers.Factory(ReviewRepository)


@router.post("/auth")
@inject
async def auth_client(
        credentials: ClientCredentials,
        client_repo: ClientRepository = Depends(Provide[Container.clients]),
) -> dict[str, str | Any]:
    client = await client_repo.get_by_credentials(
        credentials.email,
        str(hash(credentials.password)),
    )
    if client:
        access_token = await create_access_token(client)
        return {'access_token': access_token, 'client': client}
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="client with the given params not found"
    )


@router.get("/{client_id}")
@inject
async def one_client(
        client_id: int,
        client_repo: ClientRepository = Depends(Provide[Container.clients])
) -> ClientOut:
    client = await client_repo.get(client_id)
    if client:
        return client
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="client with the given Id not found"
    )


@router.post("/")
@inject
async def register_client(client: ClientIn,
                          client_repo: ClientRepository = Depends(Provide[Container.clients]),
                          ) -> dict[str, str | Any]:
    client.password_hash = str(hash(client.password))
    client.password = None
    client = await client_repo.create(client)
    access_token = await create_access_token(client)
    return {'access_token': access_token, 'client': client}


@router.put("/")
@client
@inject
async def update_client(
        client: UpdateClient,
        client_repo: ClientRepository = Depends(Provide[Container.clients]),
) -> ClientOut:
    update_data = client.update_data
    if update_data.password:
        update_data.password_hash = str(hash(update_data.password))
        update_data.password = None
    updated_client = await client_repo.update(update_data.dict(exclude_none=True))
    if updated_client:
        return updated_client
    raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="Client with the given ID not found")


@router.delete("/{client_id}")
@client
@inject
async def delete_client(
        client: IdModel,
        client_repo: ClientRepository = Depends(Provide[Container.clients]),
) -> list[ClientOut]:
    client = await client_repo.delete(client.id)
    if client:
        return client
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="client with the given Id not found"
    )


@router.post("/favourite_hospitals")
@client
@inject
async def add_hospital_to_favourite(client: AddHospitalToFavouriteClient,
                                    client_repo: ClientRepository = Depends(Provide[Container.clients]),
                                    favourite_hospitals_repo: FavouriteHospitalsRepository = Depends(
                                        Provide[Container.favourite_hospitals]),
                                    ) -> FavouriteHospital:
    favourite_hospital = client.favourite_hospital
    favourite_hospital = await favourite_hospitals_repo.create(favourite_hospital)
    if favourite_hospital:
        return favourite_hospital
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="error in adding hospital to favourite"
    )


@router.get("/favourite_hospitals/{client_id}")
@inject
async def favourite_hospitals(client: IdModel,
                              client_repo: ClientRepository = Depends(Provide[Container.clients]),
                              ) -> list[HospitalOut]:
    hospitals = await client_repo.get_favourite_hospitals(client.id)
    if hospitals:
        return hospitals
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="client with the given Id not found"
    )


@router.post("/favorite_doctors")
@client
@inject
async def add_doctor_to_favourite(
        client: FavouriteDoctorClient,
        client_repo: ClientRepository = Depends(Provide[Container.clients]),
        favorite_doctors_repo: FavoriteDoctorsRepository = Depends(
            Provide[Container.favorite_doctors]
        )
) -> list[DoctorOut]:
    favourite_doctor = client.favourite_doctor
    doctors = await favorite_doctors_repo.create(favourite_doctor)
    if doctors:
        return doctors
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="client with the given Id not found"
    )


@router.get("/favorite_doctors/{client_id}")
@inject
async def favorite_doctors(
        client_id: int,
        doctors_repo: DoctorRepository = Depends(Provide[Container.doctors]),
        client_repo: ClientRepository = Depends(Provide[Container.clients])
) -> list[DoctorOut]:
    doctors = await client_repo.get_favorite_doctors(client_id, doctors_repo)
    if doctors is not None:
        return doctors
    raise HTTPException(
        status_code=UNPROCESSABLE_ENTITY,
        detail="client with the given Id not found"
    )


@router.get("/reviews/{client_id}")
@inject
async def client_reviews(
        client_id: int,
        review_repo: ReviewRepository = Depends(Provide[Container.reviews]),
        client_repo: ClientRepository = Depends(Provide[Container.clients])
) -> list[ReviewOut]:
    reviews = await client_repo.get_reviews(
        client_id,
        review_repo,
    )
    return reviews


container = Container()
container.wire(modules=[sys.modules[__name__]])
