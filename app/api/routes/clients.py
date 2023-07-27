import sys
from http.client import UNPROCESSABLE_ENTITY
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, Depends

from app.db.repositories.client import ClientRepository
from app.db.repositories.doctor import DoctorRepository
from app.db.repositories.hospital import HospitalRepository
from app.db.repositories.favorite_doctor import FavoriteDoctorsRepository
from app.db.repositories.favourite_hospital import FavoriteHospitalsRepository
from app.models.client import ClientIn, ClientOut
from app.models.doctor import DoctorOut
from app.models.hospital import HospitalOut

router = APIRouter()


class Container(containers.DeclarativeContainer):

    clients = providers.Factory(ClientRepository)

    doctors = providers.Factory(DoctorRepository)

    hospitals = providers.Factory(HospitalRepository)

    favorite_doctors = providers.Factory(FavoriteDoctorsRepository)

    favorite_hospitals = providers.Factory(FavoriteHospitalsRepository)


@router.get("/")
@inject
async def clients_list(client_repo: ClientRepository = Depends(Provide[Container.clients])) -> list[ClientOut]:
    client = await client_repo.list()
    return client


@router.get("/{client_id}")
@inject
async def one_client(client_id: int, client_repo: ClientRepository = Depends(
                           Provide[Container.clients])) -> ClientOut:
    client = await client_repo.get(client_id)
    if client:
        return client
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="client with the given Id not found")


@router.post("/")
@inject
async def create_client(client: ClientIn, client_repo: ClientRepository = Depends(
                              Provide[Container.clients])) -> ClientOut:
    client.password_hash = str(hash(client.password))
    client.password = None
    client = await client_repo.create(client)
    return client


@router.put("/")
@inject
async def update_client(client: ClientIn, client_repo: ClientRepository = Depends(
                              Provide[Container.clients])) -> ClientOut:
    client.approved = False
    client = await client_repo.update(client)
    if client:
        return client
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="client with the given Id not found")


@router.delete("/{client_id}")
@inject
async def delete_client(client_id: int, client_repo: ClientRepository = Depends(
                              Provide[Container.clients])) -> list[ClientOut]:
    client = await client_repo.delete(client_id)
    if client:
        return client
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="client with the given Id not found")


@router.get("/favorite_hospitals/{client_id}")
@inject
async def favorite_hospitals(client_id: int,
                             hospitals_repo: FavoriteDoctorsRepository = Depends(Provide[Container.hospitals]),
                             favorite_hospitals_repo: FavoriteDoctorsRepository = Depends(Provide[Container.favorite_hospitals]),
                             client_repo: ClientRepository = Depends(Provide[Container.clients])
                             ) -> list[HospitalOut]:
    hospitals = await client_repo.get_favorite_hospitals(client_id, hospitals_repo, favorite_hospitals_repo._table)
    if hospitals:
        return hospitals
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="client with the given Id not found")


@router.post("/favorite_hospitals/{client_id}")
@inject
async def favorite_hospitals(client_id: int,
                             hospitals_repo: FavoriteDoctorsRepository = Depends(Provide[Container.hospitals]),
                             favorite_hospitals_repo: FavoriteDoctorsRepository = Depends(Provide[Container.favorite_hospitals]),
                             client_repo: ClientRepository = Depends(Provide[Container.clients])
                             ) -> list[HospitalOut]:
    hospitals = await client_repo.get_favorite_hospitals(client_id, hospitals_repo, favorite_hospitals_repo._table)
    if hospitals:
        return hospitals
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="client with the given Id not found")


@router.delete("/favorite_hospitals/{client_id}")
@inject
async def favorite_hospitals(client_id: int,
                             hospitals_repo: FavoriteDoctorsRepository = Depends(Provide[Container.hospitals]),
                             favorite_hospitals_repo: FavoriteDoctorsRepository = Depends(Provide[Container.favorite_hospitals]),
                             client_repo: ClientRepository = Depends(Provide[Container.clients])
                             ) -> list[HospitalOut]:
    hospitals = await client_repo.get_favorite_hospitals(client_id, hospitals_repo, favorite_hospitals_repo._table)
    if hospitals:
        return hospitals
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="client with the given Id not found")


@router.get("/favorite_doctors/{client_id}")
@inject
async def favorite_doctors(client_id: int,
                           doctors_repo: FavoriteDoctorsRepository = Depends(Provide[Container.doctors]),
                           favorite_doctors_repo: FavoriteDoctorsRepository = Depends(Provide[Container.favorite_doctors]),
                           client_repo: ClientRepository = Depends(Provide[Container.clients])) -> list[DoctorOut]:
    doctors = await client_repo.get_favorite_doctors(client_id, doctors_repo, favorite_doctors_repo._table)
    if doctors:
        return doctors
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="client with the given Id not found")


container = Container()
container.wire(modules=[sys.modules[__name__]])
