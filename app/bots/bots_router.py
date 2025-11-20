from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db.models import Bot, User
from app.core.db.session import session_provider
from app.core.db_queries.bots import get_bot_by_id, get_bots_from_db
from app.core.utils.auth import get_current_user

from .schemas import BotRequest, BotResponse

BASE_PREFIX = "/bots"
bots_router = APIRouter(
    prefix=BASE_PREFIX,
    tags=["bots"],
)

@bots_router.get(
    "/",
    response_model=list[BotResponse]
)
async def get_all_bots(
        bots: Annotated[list[Bot], Depends(get_bots_from_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    return bots

@bots_router.get(
    "/{bot_id}",
    response_model=BotResponse
)
async def get_bot(
        bot: Annotated[Bot, Depends(get_bot_by_id)],
        user: Annotated[User, Depends(get_current_user)]
):
    return bot

@bots_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Bot created"}
    }
)
async def create_bot(
        data: BotRequest,
        user: Annotated[User, Depends(get_current_user)],
):
    bot = Bot(**data.model_dump())
    user.bots.append(bot)
    return {"message": "Bot created"}

@bots_router.post(
    "/{bot_id}",
)
async def acquire_lock(
        bot: Annotated[Bot, Depends(get_bot_by_id)],
        user: Annotated[User, Depends(get_current_user)],
):
    if bot.locktime:
        return {"message": "Bot already locked"}
    bot.locktime = datetime.now(timezone.utc)
    return {"message": "Bot locked"}

@bots_router.patch(
    "/{bot_id}",
)
async def release_lock(
        bot: Annotated[Bot, Depends(get_bot_by_id)],
        user: Annotated[User, Depends(get_current_user)],
):
    if not bot.locktime:
        return {"message": "Bot already unlocked"}
    bot.locktime = None
    return {"message": "Bot unlocked"}
