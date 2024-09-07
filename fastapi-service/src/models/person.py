from typing import Dict, List, Union

from pydantic import BaseModel


class Person(BaseModel):
    id: str
    full_name: str
    films: Union[List[Dict[str, Union[List[str], str]]], None] = None
