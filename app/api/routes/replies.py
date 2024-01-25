from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.db.repositories.client import ClientRepository
from app.db.repositories.reply import ReplyRepository
from app.models.reply import ReplyIn, ReplyOut

router = APIRouter()


class Container(containers.DeclarativeContainer):

    replies = providers.Factory(ReplyRepository)


@router.post("/")
@inject
async def create_reply(reply: ReplyIn) -> ReplyOut:
    rr = ReplyRepository()
    reply = await rr.create(reply)
    return reply


@router.get("/{review_id}")
@inject
async def review_replies(review_id: int) -> list[ReplyOut]:
    rr = ReplyRepository()
    review = await rr.list(review_id)
    return review


@router.get("/{reply_id}")
@inject
async def delete_reply(reply_id: int,
                       reply_repo: ReplyRepository = Depends(Provide[Container.replies])
                       ) -> list[ReplyOut]:
    rr = ReplyRepository()
    review = await rr.delete(reply_id)
    return review
