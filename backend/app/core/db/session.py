from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(
    "postgresql+psycopg2://user:password@localhost/bots.db",
)

def create_session():
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


def session_provider(
        session: Annotated[Session, Depends(create_session)]
):
    return session

