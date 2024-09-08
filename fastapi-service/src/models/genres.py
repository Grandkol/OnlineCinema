from typing import Union

from pydantic import BaseModel


class BaseGenre(BaseModel):
    id: str
    name: str
    description: Union[str, None] = None


class Genre(BaseGenre):
    movies: list[dict[str, str]]
