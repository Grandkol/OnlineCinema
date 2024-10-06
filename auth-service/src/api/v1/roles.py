from fastapi import APIRouter, Depends
from models.roles import Roles, Permissions
from schemas.roles import Role, RoleCreate, PermissionDb, PermissionCreate
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
    role_dto['permissions'][0] = UUID(role_dto['permissions'][0])
    stm = select(Permissions).where(Permissions.id==role_dto['permissions'][0])
    perm = await db.execute(stm)
    p1 = perm.scalars().first()
    role_dto['permissions'][0] = p1
    role = Roles(**role_dto)
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role



@router.post("/role/permissions/create", response_model=PermissionDb)
async def create_permission(permission_create: PermissionCreate, db: AsyncSession = Depends(get_session)) -> PermissionDb:
    permission_dto = jsonable_encoder(permission_create)
    

@router.get("/roles", response_model=PermissionDb)
async def get_roles(db: AsyncSession = Depends(get_session)):
    pass


@router.patch("/roles/{role_id}", response_model=PermissionDb)
async def update_role(role_id: UUID):
    pass


@router.delete("/role/{role_id}", status_code=HTTPStatus.OK)
async def delete_role(role_id: UUID, db: AsyncSession = Depends(get_session)) -> dict:
    pass
    return {"message": "Permission was deleted succesfully!"}


@router.get("/role/permissions/", response_model=PermissionDb)
async def create_permission(permission_create: PermissionCreate, db: AsyncSession = Depends(get_session)) -> PermissionDb:
    pass

@router.delete("/role/permissions/{permission_id}", status_code=HTTPStatus.OK)
async def delete_permission(permission_id: UUID, db: AsyncSession = Depends(get_session)) -> dict:
    pass
    return {"message": "Permission was deleted succesfully!"}