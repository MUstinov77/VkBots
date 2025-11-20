from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import TIMESTAMP, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    relationship
    )

from app.bots.enum import BotDomain, BotEnv

Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] =  mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=datetime.now(timezone.utc)
    )

    bots: Mapped[list["Bot"]] = relationship("Bot", back_populates="user")


class Bot(Base):

    __tablename__ = "bots"

    id: Mapped[UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=datetime.now(timezone.utc)
    )
    env: Mapped[str] = mapped_column(Enum(BotEnv))
    domain: Mapped[str] = mapped_column(Enum(BotDomain))
    locktime: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    user: Mapped[User] = relationship("User", back_populates="bots")
