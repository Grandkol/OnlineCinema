from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi.encoders import jsonable_encoder
from rest_framework import status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.entity import UserInDB, UserCreate, TokenInfo
from models import User
from core import utils

# router = APIRouter()


# @router.post("/reg", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
# async def create_user(
#     user_create: UserCreate, db: AsyncSession = Depends(get_session)
# ) -> UserInDB:
#     user_dto = jsonable_encoder(user_create)
#     user = User(**user_dto)
#     db.add(user)
#     await db.commit()
#     await db.refresh(user)
#     return user


# @router.post("/login", response_model=TokenInfo)
# def auth_user(user: User, db: AsyncSession = Depends(get_session)):
#     access_token = utils.encode_jwt()
#     # jwt_payload =
#     return TokenInfo(
#         access_token=access_token,
#         token_type="Bearer",
#     )
