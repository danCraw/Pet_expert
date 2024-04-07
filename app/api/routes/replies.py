import sys
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.db.repositories.reply import ReplyRepository
from app.models.auth.base import IdModel
from app.models.auth.reply import CreateReply
from app.models.reply import ReplyIn, ReplyOut
from app.redis.clients.auth import client
from app.redis.doctors.auth import doctor

router = APIRouter()


class Container(containers.DeclarativeContainer):
    replies = providers.Factory(ReplyRepository)


@router.post("/")
@inject
async def create_reply(reply: ReplyIn,
                       reply_repo: ReplyRepository = Depends(Provide[Container.replies])
                       ) -> ReplyOut:
    reply = await reply_repo.create(reply)
    return reply


@router.post("/client")
@client
async def create_client_reply(reply: CreateReply) -> ReplyOut:
    return await create_reply(reply.reply)


@router.post("/doctor ")
@doctor
async def create_doctor_reply(reply: CreateReply) -> ReplyOut:
    return await create_reply(reply.reply)


@router.get("/{review_id}")
@inject
async def review_replies(review_id: int,
                         reply_repo: ReplyRepository = Depends(Provide[Container.replies])
                         ) -> list[ReplyOut]:
    reply = await reply_repo.list(review_id)
    return reply


@router.get("/{reply_id}")
@inject
async def delete_reply(reply_id: int,
                       reply_repo: ReplyRepository = Depends(Provide[Container.replies])
                       ) -> ReplyOut:
    reply = await reply_repo.delete(reply_id)
    return reply


@router.delete("/client/{reply_id}")
@client
async def delete_client_reply(reply_id) -> ReplyOut:
    return await delete_reply(reply_id.id)


@router.delete("/doctor/{reply_id}")
@doctor
async def delete_doctor_reply(reply_id) -> ReplyOut:
    return await delete_reply(reply_id.id)


container = Container()
container.wire(modules=[sys.modules[__name__]])
