from fastapi import APIRouter, Depends
from models.roles import Roles, Permissions
from schemas.roles import Role, RoleCreate
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import get_session
from http import HTTPStatus
from uuid import UUID
from sqlalchemy import select

router = APIRouter()

@router.post("/create", response_model=Role, status_code=HTTPStatus.CREATED)
async def create_role(role_create: RoleCreate, db: AsyncSession = Depends(get_session)) -> Role:
    role_dto = jsonable_encoder(role_create)
    # role_dto['permissions'][0] = UUID(role_dto['permissions'][0])
    # stm = select(Permissions).where(Permissions.id==role_dto['permissions'][0])
    # perm = await db.execute(stm)
    # p1 = perm.scalars().first()
    # print(p1)
    # role_dto['permissions'][0] = p1
    role = Roles(**role_dto)
    print(111)
    print(role.__dict__)
    db.add(role)
    print(2222)
    await db.commit()
    await db.refresh(role)
    print(333333333333333333333333)
    return role
