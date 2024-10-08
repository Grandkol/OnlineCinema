from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from abc import ABC, abstractmethod
from db.postgres import DatabaseHelper
from models.roles import Permissions, Roles, Category
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy import select

from core import settings


db = DatabaseHelper(str(settings.db.url)) # Укажи URL

class AbstractService(ABC):
    
    @abstractmethod
    def create_item(self):
        pass

    @abstractmethod
    def get_item(self):
        pass

    @abstractmethod
    def add_to_db(self):
        pass


class DatabaseService:

    def __init__(self, db):
        self.db = db

    async def create_role(self, data: dict):

        if data['permissions']:
            stm = select(Permissions).where(Permissions.id.in_(data['permissions']))
            perm = await self.db.execute(stm)
            permissions = perm.scalars().all()
            if not permissions:
                return False
            data['permissions'] = permissions
        role = Roles(**data)
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role


    async def create_permission(self, data: dict):
        print(data)
        stm = select(Category).where(Category.id==data['category'])
        perm = await self.db.execute(stm)
        category = perm.scalars().first()
        data['category'] = category
        permission = Permissions(**data)
        self.db.add(permission)
        await self.db.commit()
        await self.db.refresh(permission)
        permission.category_title = category.title
        return permission

    def get_item(self, statement):
        pass
    



    def add_to_db(self, data: dict | list[dict], model: DeclarativeMeta):
        if isinstance(data, list):
            for item in data:
                self.create_item(item, model)
        else:
            self.create_item(data)
    
    def create_item(self, model = None, statement = None):
        pass


    def create_item(self, data: dict):
        
        self.db.add(data)

    def create_many(self, data: list[dict]):
        pass



class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db


    def get_single_role(self, role_id: str):
        pass

    def get_all_roles(self):
        pass

    def create_role(self, data:dict):
        pass


    def modify_role(self, role_id: str, data: dict):
        pass

    def delete_role(self, role_id: str):
        pass



def get_db_service(db: AsyncSession = db):
    return DatabaseService(db)