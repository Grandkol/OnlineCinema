from typing import Annotated
import datetime
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi.encoders import jsonable_encoder
from rest_framework import status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from schemas import UserInDB, UserCreate, TokenInfo, AuthUser, RefreshToken
from models import User
from core import utils
from db import db_helper
from services.auth import create_user as crud_create_user
from services.auth import (
    get_token,
    get_current_active_auth_user,
    get_current_token_payload,
    _get_tokens_from_refresh_token,
    _user_auth_logout
)

router = APIRouter()


@router.post("/reg", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: Annotated[UserCreate, Depends(UserCreate)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user = await crud_create_user(session=session, user_create=user_create)
    return user


@router.post("/login", response_model=TokenInfo, status_code=status.HTTP_200_OK)
async def auth_user(
    data: AuthUser = Depends(AuthUser),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_token(data=data, session=session)

@router.post("/refresh", response_model=TokenInfo, status_code=status.HTTP_200_OK)
async def auth_refresh_jwt(
        refresh_token,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    return await _get_tokens_from_refresh_token(refresh_token=refresh_token, session=session)



@router.get("/user/me/")
def user_self_info(
    user: User = Depends(get_current_active_auth_user),
    payload: dict = Depends(get_current_token_payload),
):
    iat = payload.get("iat")
    readable = datetime.datetime.fromtimestamp(iat).strftime("%Y-%m-%d %H:%M:%S")
    return {"login": user.login,
            "email": user.email,
            "logged_in": readable,}


@router.post("/logout")
def user_logout(
        user: User = Depends(_user_auth_logout),
):
    return f"user: {user.login} was logged out"

@router.patch("/user")
def user_auth_patch():
    pass
