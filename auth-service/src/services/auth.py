from typing import Sequence
import uuid
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
from sqlalchemy import update
from werkzeug.security import check_password_hash, generate_password_hash
from core import settings, encode_access_token, encode_refresh_token, decode_token
from models import User
from schemas import UserCreate
from sqlalchemy.testing.config import ident
from db import db_helper
from sqlalchemy.testing.suite.test_reflection import users
from services import redis
from schemas import UserInDB, UserCreate, TokenInfo, AuthUser, RefreshToken


http_bearer = HTTPBearer()

ACCESS_EXPIRY = timedelta(minutes=15)
REFRESH_EXPIRY = timedelta(minutes=1000)


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


async def validate_access_token(payload: str):
    key = f"{payload["token_id"]}:access_denied"
    if await redis._get_from_redis(key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are logged out and don't have access to this information. Please Log In again",
        )


async def _get_user_token(user: User, refresh_token=None):
    access_payload = {
        "token_id": str(uuid.uuid4()),
        "sub": str(user.id),
        "role": user.role,
        "type": "access",
    }
    refresh_payload = {
        "token_id": str(uuid.uuid4()),
        "sub": str(user.id),
        "type": "refresh",
    }

    key = f"{user.id}:refresh_token"
    access_token = await encode_access_token(access_payload, ACCESS_EXPIRY)

    if not refresh_token:
        refresh_token = await encode_refresh_token(refresh_payload, REFRESH_EXPIRY)

    await redis._put_to_redis(key=key, token=refresh_token)
    print(await redis._get_redis_keys())

    return {"access_token": access_token, "refresh_token": refresh_token}


async def _get_tokens_from_refresh_token(
    refresh_token: HTTPAuthorizationCredentials = Depends(TokenInfo),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    decoded = decode_token(refresh_token)
    if decoded["type"] != "refresh":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="It is not a valid refresh token",
        )
    User_id = decoded["sub"]
    user = await session.execute(select(User).where(User.id == User_id))
    user = user.scalars().one()

    return await _get_user_token(user=user)


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> User:
    token = credentials.credentials
    payload = decode_token(token=token)
    await validate_access_token(payload)
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

    User_id: str | None = payload.get("sub")
    user = await session.execute(select(User).where(User.id == User_id))
    user = user.scalars().one()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid. User not found",
        )

    return user


def get_current_active_auth_user(user: User = Depends(get_current_auth_user)):

    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Inactive user",
    )


async def user_auth_logout(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    token_type = payload.get("type")
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authentified to logout, please proceed with login",
        )

    User_id: str | None = payload.get("sub")

    user = await session.execute(select(User).where(User.login == User_id))
    user = user.scalars().one()
    key_refresh_delete = f"{user.id}:refresh_token"
    key_access_denied = f"{payload.get('token_id')}:access_denied"
    access_token_denied = await encode_access_token(payload, ACCESS_EXPIRY)

    if await redis._get_from_redis(key_access_denied):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="You had already logged out.",
        )

    await redis._put_to_redis(key=key_access_denied, token=access_token_denied)
    await redis._delete_from_redis(key=key_refresh_delete)

    return user


async def user_patch_data(
    user_data: UserCreate,
    payload: dict,
    session: AsyncSession,
):
    user_id = payload.get("sub")
    user = await session.execute(select(User).where(User.id == user_id))
    user = user.scalars().one()

    await session.execute(
        update(User).where(User.login == user.login).values(login=user_data.login)
    )
    hashed_password = generate_password_hash(user_data.password)

    await session.execute(
        update(User)
        .where(User.password == user.password)
        .values(password=hashed_password)
    )
    await session.execute(
        update(User)
        .where(User.first_name == user.first_name)
        .values(first_name=user_data.first_name)
    )
    await session.execute(
        update(User)
        .where(User.last_name == user.last_name)
        .values(last_name=user_data.last_name)
    )

    await session.commit()
    await session.refresh(user)

    return {
        "login": user.login,
        "first_name": user.first_name,
        "password": user.password,
        "last_name": user.last_name,
    }
