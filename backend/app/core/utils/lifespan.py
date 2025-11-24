from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.core.db.models import Base
from backend.app.core.db.session import engine


def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    return