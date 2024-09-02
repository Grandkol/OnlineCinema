from pydantic import BaseModel
from typing import List


class Genre(BaseModel):
    id: str
    name: str
    description: str = None
