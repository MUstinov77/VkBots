from datetime import datetime

from pydantic import BaseModel

from .enum import BotDomain, BotEnv


class BotRequest(BaseModel):
    login: str
    password: str
    env: BotEnv
    domain: BotDomain

class BotResponse(BotRequest):

    id: int
    locktime: datetime | None = None