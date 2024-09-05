from __future__ import annotations
from typing import List,Dict

from typing import Union
from pydantic import BaseModel


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: Union[float, None] = None
    description: Union[str, None] = None
    genres: Union[List[Dict], None] = None
    actors: Union[List[Dict], None] = None
    writers: Union[List[Dict], None] = None
    directors: Union[List[Dict], None] = None


class FilmList(BaseModel):
    id: str
    title: str
    imdb_rating: Union[float, None] = None