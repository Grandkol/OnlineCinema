from typing import Union

from pydantic import BaseModel


class Person(BaseModel):
    id: str
    full_name: str
    films: Union[list[dict[str, Union[list[str], str]]], None] = None
