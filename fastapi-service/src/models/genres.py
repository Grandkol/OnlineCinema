from typing import Dict, List, Union

from pydantic import BaseModel


class BaseGenre(BaseModel):
    id: str
    name: str
    description: Union[str, None] = None


class Genre(BaseGenre):
    movies: List[Dict[str, str]]
