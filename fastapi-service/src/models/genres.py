from pydantic import BaseModel


class Genre(BaseModel):
    id: str
    name: str
    description: str = None


class FilmGenres(BaseModel):
    name: str
