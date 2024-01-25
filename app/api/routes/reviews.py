import sys
from http.client import UNPROCESSABLE_ENTITY

from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, Depends

from app.db.repositories.client import ClientRepository
from app.db.repositories.doctor import DoctorRepository
from app.db.repositories.hospital import HospitalRepository
from app.db.repositories.reply import ReplyRepository
from app.db.repositories.review import ReviewRepository
from app.db.repositories.visit import VisitRepository
from app.models.review import ReviewIn
from app.models.review import ReviewOut

router = APIRouter()


class Container(containers.DeclarativeContainer):
    reviews = providers.Factory(ReviewRepository)

    reply = providers.Factory(ReplyRepository)

    hospitals = providers.Factory(HospitalRepository)

    visits = providers.Factory(VisitRepository)

    doctors = providers.Factory(DoctorRepository)

    clients = providers.Factory(ClientRepository)


@router.get("/")
@inject
async def reviews_list(
        review_repo: ReviewRepository = Depends(Provide[Container.reviews])
) -> list[ReviewOut]:
    review = await review_repo.list()
    return review


@router.get("/{review_id}")
@inject
async def one_review(
        review_id: int,
        review_repo: ReviewRepository = Depends(Provide[Container.reviews]),
) -> ReviewOut:
    review = await review_repo.get(review_id)
    if review:
        return review
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="review with the given Id not found")


@router.post("/")
@inject
async def create_review(
        review: ReviewIn,
        review_repo: ReviewRepository = Depends(Provide[Container.reviews])
) -> ReviewOut:
    review = await review_repo.create(review)
    return review


@inject
async def delete_review(
        review_id: int,
        review_repo: ReviewRepository = Depends(Provide[Container.reviews])
) -> list[ReviewOut]:
    review = await review_repo.delete(review_id)
    if review:
        return review
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="review with the given Id not found")


container = Container()
container.wire(modules=[sys.modules[__name__]])
