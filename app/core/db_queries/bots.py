from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db.models import Bot
from app.core.db.session import session_provider


def get_bots_from_db(
        session: Annotated[Session, Depends(session_provider)]
):
    query = session.execute(select(Bot))
    result = query.scalars().all()
    return result

def get_bot_by_id(
        bot_id: UUID,
        session: Annotated[Session, Depends(session_provider)],
):
    query = select(Bot).where(Bot.id == bot_id)
    result = session.execute(query)
    return result.scalar_one_or_none()