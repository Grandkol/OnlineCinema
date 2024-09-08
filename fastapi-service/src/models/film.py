from __future__ import annotations

from typing import Union

from pydantic import BaseModel


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: Union[float, None] = None
    description: Union[str, None] = None
    genres: Union[list[dict], None] = None
    actors: Union[list[dict], None] = None
    writers: Union[list[dict], None] = None
    directors: Union[list[dict], None] = None


class FilmList(BaseModel):
    id: str
    title: str
    imdb_rating: Union[float, None] = None
