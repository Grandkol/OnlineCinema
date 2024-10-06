from typing import Sequence

from blib2to3.pgen2.tokenize import TokenInfo
from django.contrib.auth import login
from dns.e164 import query
from fastapi.params import Depends
from rest_framework import status
from fastapi.exceptions import HTTPException
from fastapi import Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from datetime import timedelta, datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core import settings, encode_access_token, encode_refresh_token, decode_token
from models import User
from schemas import UserCreate
from sqlalchemy.testing.config import ident
from db import db_helper
from sqlalchemy.testing.suite.test_reflection import users


http_bearer = HTTPBearer()


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_token(data, session):
    user = await session.execute(select(User).where(User.login == data.login))
    user = user.scalars().one()

    if not user.check_password(data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid login Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await _get_user_token(user=user)


async def _get_user_token(user: User, refresh_token=None):
    access_payload = {"sub": user.login, "role": user.role, "type": "access"}
    refresh_payload = {
        "sub": user.login,
        "type": "refresh",
    }

    access_token_expiry = timedelta(minutes=15)
    refresh_token_expiry = timedelta(minutes=1000)
    access_token = await encode_access_token(access_payload, access_token_expiry)
    if not refresh_token:
        refresh_token = await encode_refresh_token(
            refresh_payload, refresh_token_expiry
        )

    return {"access_token": access_token, "refresh_token": refresh_token}


async def _get_tokens_from_refresh_token(
        refresh_token: HTTPAuthorizationCredentials = Depends(TokenInfo),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    decoded = decode_token(refresh_token)
    if decoded["type"] != "refresh":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="It is not a valid refresh token",
        )
    login = decoded["sub"]
    user = await session.execute(select(User).where(User.login == login))
    user = user.scalars().one()

    return await _get_user_token(user=user)


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> User:
    token = credentials.credentials
    payload = decode_token(token=token)
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    token_type = payload.get("type")
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    login: str | None = payload.get("sub")
    user = await session.execute(select(User).where(User.login == login))
    user = user.scalars().one()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid. User not found",
        )

    return user


def get_current_active_auth_user(
        user: User = Depends(get_current_auth_user)
):

    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Inactive user",
    )
