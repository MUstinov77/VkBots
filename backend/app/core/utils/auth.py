from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.api.auth.schemas import TokenData
from backend.app.core.db.models import User
from backend.app.core.db.session import session_provider
from backend.app.core.utils.encrypt import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "6a6b44234fa959e4205b61a20bc1ffda71448cfd58fc3c94726b91762c2eb447"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


def get_user(
        username: str,
        session: Session,
):
    query = select(User).where(User.username == username)
    result= session.execute(query)
    return result.scalar_one_or_none()

async def authenticate_user(
        username: str,
        password: str,
        session: Session
):
    user = get_user(username, session)
    if not user:
        return {"message": "User not found"}
    if not await verify_password(password, user.password):
        return {"message": "Incorrect password"}
    return user

def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Annotated[Session, Depends(session_provider)]
):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.username, session)
    if not user:
        raise credentials_exception
    return user