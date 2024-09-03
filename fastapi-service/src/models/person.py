from pydantic import BaseModel

from typing import Union, List, Dict

class Person(BaseModel):
    id: str
    full_name: str
    films: Union[List[Dict[str, List[str]]], None] = None
