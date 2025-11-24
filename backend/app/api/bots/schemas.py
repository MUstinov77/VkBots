from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from backend.app.api.bots.enum import BotDomain, BotEnv


class BotRequest(BaseModel):
    login: str
    password: str
    env: BotEnv
    domain: BotDomain

class BotResponse(BotRequest):

    id: UUID
    created_at: datetime
    locktime: datetime | None = None