from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi.encoders import jsonable_encoder
from rest_framework import status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import UserInDB, UserCreate
from models import User
from core import utils
from db import db_helper
from services.auth import create_user as crud_create_user

router = APIRouter()


@router.post("/reg", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_create: UserCreate,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]
):

    user = await crud_create_user(session=session, user_create=user_create)
    return user



# @router.post("/login", response_model=TokenInfo)
# def auth_user(user: User, db: AsyncSession = Depends(get_session)):
#     access_token = utils.encode_jwt()
#     # jwt_payload =
#     return TokenInfo(
#         access_token=access_token,
#         token_type="Bearer",
#     )
