from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi.encoders import jsonable_encoder
from rest_framework import status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.entity import UserInDB, UserCreate
from db.postgres import get_session
from models.entity import User

router = APIRouter()

@router.post('/reg', response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, db: AsyncSession = Depends(get_session)) -> UserInDB:
    user_dto = jsonable_encoder(user_create)
    user = User(**user_dto)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# @router.post('/login')
# def auth_user(user: ):
#     pass
