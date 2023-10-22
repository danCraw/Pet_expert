import sys
from http.client import UNPROCESSABLE_ENTITY

from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, Depends

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


@router.get("/")
@inject
async def reviews_list(review_repo: ReviewRepository = Depends(Provide[Container.reviews])) -> list[ReviewOut]:
    review = await review_repo.list()
    return review


@router.get("/{review_id}")
@inject
async def one_review(review_id: int, review_repo: ReviewRepository = Depends(
                           Provide[Container.reviews])) -> ReviewOut:
    review = await review_repo.get(review_id)
    if review:
        return review
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="review with the given Id not found")


@router.post("/")
@inject
async def create_review(review: ReviewIn,
                        review_repo: ReviewRepository = Depends(Provide[Container.reviews]),
                        visits_repo: ReviewRepository = Depends(Provide[Container.visits]),
                        doctor_repo: ReviewRepository = Depends(Provide[Container.doctors]),
                        hospitals_repo: ReviewRepository = Depends(Provide[Container.hospitals])
                        ) -> ReviewOut:
    review = await review_repo.create(review, visits_repo._table, doctor_repo._table, hospitals_repo._table)
    return review


@router.post("/reply/{review_id}")
@inject
async def reply_to_review(review_id: int, review: ReviewIn,
                          review_repo: ReviewRepository = Depends(Provide[Container.reviews]),
                          reply_repo: ReplyRepository = Depends(Provide[Container.reply])) -> ReviewOut:
    review = await review_repo.reply(review_id, review, reply_repo)
    return review


@inject
async def delete_review(review_id: int, review_repo: ReviewRepository = Depends(
    Provide[Container.reviews])) -> list[ReviewOut]:
    review = await review_repo.delete(review_id)
    if review:
        return review
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="review with the given Id not found")


container = Container()
container.wire(modules=[sys.modules[__name__]])
