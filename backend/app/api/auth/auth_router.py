from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from backend.app.core.db.models import User
from backend.app.core.db.session import session_provider

from ...core.utils.auth import (
    ACCESS_TOKEN_EXPIRE_DAYS,
    authenticate_user,
    create_access_token
    )
from ...core.utils.encrypt import get_hashed_password
from .schemas import Token, UserSignupLoginSchema

BASE_PREFIX = "/auth"

auth_router = APIRouter(
    prefix=BASE_PREFIX,
    tags=["auth"],
)

@auth_router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED
)
async def signup(
        data: UserSignupLoginSchema,
        session: Annotated[Session, Depends(session_provider)]
):
    user_data = data.model_dump()
    hashed_password = await get_hashed_password(user_data.pop("password"))
    user = User(**user_data)
    user.password = hashed_password
    session.add(user)
    return {"message": "User created"}


@auth_router.post(
    "/login",
    response_model=Token,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid credentials"}
    }
)
async def login(
        login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[Session, Depends(session_provider)]
):
    user = await authenticate_user(
        login_data.username,
        login_data.password,
        session
    )
    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Invalid credentials"}
        )
    token_timedelta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=token_timedelta)

    return Token(access_token=access_token, token_type="bearer")