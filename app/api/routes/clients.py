import sys
from http.client import UNPROCESSABLE_ENTITY
from typing import List
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, Depends

from app.db.repositories.client import ClientRepository
from app.models.client import ClientIn, ClientOut, ClientsList

router = APIRouter()


class Container(containers.DeclarativeContainer):

    clients = providers.Factory(ClientRepository)

    clients_specializations = providers.Factory(ClientSpecializationsRepository)

    specializations = providers.Factory(SpecializationRepository)


@router.get("/")
@inject
async def clients_list(clients_list: ClientsList, client_repo: ClientRepository = Depends(Provide[Container.clients]),
                             clients_specializations_repo: ClientSpecializationsRepository = Depends(
                                 Provide[Container.clients_specializations]),
                             specializations_repo: SpecializationRepository = Depends(
                                 Provide[Container.specializations])
                             ) -> List[ClientOut]:
    client = await client_repo.approved_clients(clients_list.start, clients_list.amount,
                                                                  specializations_repo._table, clients_specializations_repo._table)
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
                              Provide[Container.clients])) -> List[ClientOut]:
    client = await client_repo.delete(client_id)
    if client:
        return client
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="client with the given Id not found")


container = Container()
container.wire(modules=[sys.modules[__name__]])
