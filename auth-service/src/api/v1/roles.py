from fastapi import APIRouter, Depends, HTTPException
from models.roles import Roles, Permissions
from schemas.roles import Role, RoleCreate, PermissionDb, PermissionCreate
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from service.role import DatabaseService, get_db_service
from db.postgres import get_session
from http import HTTPStatus
from uuid import UUID
from sqlalchemy import select
from service.role import get_db_service, DatabaseService

router = APIRouter()


@router.post("/create", response_model=Role, status_code=HTTPStatus.CREATED)
async def create_role(role_create: RoleCreate, db: DatabaseService = Depends(get_db_service)) -> Role:
    role_dto = jsonable_encoder(role_create)
    role = await db.create_role(role_dto)
    if not role:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Wrong permission")

    return role



@router.post("/role/permissions/create", response_model=PermissionDb)
async def create_permission(permission_create: PermissionCreate | list[PermissionCreate], db_service: DatabaseService = Depends(get_session)) -> PermissionDb:

    permission_dto = jsonable_encoder(permission_create)
    permission = await db_service.create_permission(permission_dto)
    return permission
    
    

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