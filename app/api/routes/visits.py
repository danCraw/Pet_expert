import sys
from http.client import UNPROCESSABLE_ENTITY

from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, Depends

from app.db.repositories.reply import ReplyRepository
from app.db.repositories.visit import VisitRepository
from app.models.visit import VisitIn
from app.models.visit import VisitOut

router = APIRouter()


class Container(containers.DeclarativeContainer):

    visits = providers.Factory(VisitRepository)

    reply = providers.Factory(ReplyRepository)


@router.get("/")
@inject
async def visits_list(visit_repo: VisitRepository = Depends(Provide[Container.visits])) -> list[VisitOut]:
    visit = await visit_repo.list()
    return visit


@router.get("/{visit_id}")
@inject
async def one_visit(visit_id: int, visit_repo: VisitRepository = Depends(
                           Provide[Container.visits])) -> VisitOut:
    visit = await visit_repo.get(visit_id)
    if visit:
        return visit
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="visit with the given Id not found")


@router.post("/")
@inject
async def create_visit(visit: VisitIn, visit_repo: VisitRepository = Depends(
                              Provide[Container.visits])) -> VisitOut:
    visit = await visit_repo.create(visit)
    return visit


container = Container()
container.wire(modules=[sys.modules[__name__]])
