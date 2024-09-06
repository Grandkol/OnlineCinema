from pydantic import BaseModel
from typing import List, Union, Dict



class BaseGenre(BaseModel):
    id: str
    name: str
    description: Union[str, None] = None


class Genre(BaseGenre):
    movies: List[Dict[str, str]]
