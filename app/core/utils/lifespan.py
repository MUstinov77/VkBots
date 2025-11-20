from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.db.models import Base
from app.core.db.session import engine


def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # drop_db()
    return