from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from sqlalchemy.orm.decl_api import DeclarativeMeta


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

    