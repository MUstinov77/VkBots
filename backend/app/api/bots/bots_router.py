from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlalchemy.orm import Session

from backend.app.api.bots.enum import LockAction
from backend.app.core.db.models import Bot, User
from backend.app.core.db.session import session_provider
from backend.app.core.db_queries.bots import get_bot_by_id, get_bots_from_db
from backend.app.core.utils.auth import get_current_user

from .schemas import BotRequest, BotResponse

BASE_PREFIX = "/bots"
bots_router = APIRouter(
    prefix=BASE_PREFIX,
    tags=["bots"],
    dependencies=(
        Depends(get_current_user),
    )
)

@bots_router.get(
    "/",
    response_model=list[BotResponse]
)
async def get_all_bots(
        bots: Annotated[list[Bot], Depends(get_bots_from_db)],
):
    return bots

@bots_router.get(
    "/{bot_id}",
    response_model=BotResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Bot not found"}
    }
)
async def get_bot(
        bot: Annotated[Bot, Depends(get_bot_by_id)],
):
    if not bot:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Bot not found"}
        )
    return bot

@bots_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=BotResponse
)
async def create_bot(
        data: BotRequest,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[Session, Depends(session_provider)],
):
    bot = Bot(**data.model_dump())
    user.bots.append(bot)
    session.commit()
    return bot

@bots_router.delete(
    "/{bot_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Bot not found"},
        status.HTTP_403_FORBIDDEN: {"description": "Unable to delete bot"}
    }
)
async def delete_bot(
        bot: Annotated[Bot, Depends(get_bot_by_id)],
        user: Annotated[User, Depends(get_current_user)],
):
    if not bot:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Bot not found"}
        )
    if bot.user_id != user.id:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "Unable to delete bot"}
        )
    user.bots.remove(bot)
    return {"message": "Bot deleted"}

@bots_router.post(
    "/{bot_id}",
)
async def acquire_or_release_lock(
        bot: Annotated[Bot, Depends(get_bot_by_id)],
        action: LockAction = LockAction.acquire
):
    match action:
        case LockAction.acquire:
            if bot.locktime:
                return {"message": "Bot already locked"}
            bot.locktime = datetime.now(timezone.utc)
            return {"message": "Bot locked"}
        case LockAction.release:
            if not bot.locktime:
                return {"message": "Bot already unlocked"}
            bot.locktime = None
            return {"message": "Bot unlocked"}

@bots_router.patch(
    "/{bot_id}",
    response_model=BotResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Bot not found"},
        status.HTTP_403_FORBIDDEN: {"description": "Cant change other users bots"}
    }
)
async def update_bot(
        bot: Annotated[Bot, Depends(get_bot_by_id)],
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[Session, Depends(session_provider)],
        data: BotRequest
):
    if not bot:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Bot not found"}
        )
    if user.id != bot.user_id:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "Cant change other users bots"}
        )
    new_data = data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )
    session.execute(
        update(Bot).where(Bot.id == bot.id).values(**new_data)
    )
    return bot