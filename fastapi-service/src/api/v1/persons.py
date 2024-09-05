from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from models.person import Person
from services.person import PersonService, get_person_service


router = APIRouter()


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)):
    person = await person_service.get_by_id(person_id=person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return Person(id=person.id, full_name=person.full_name, films=person.films)

# @router.get('/persons', response_model=list[Person])
# async def persons_list(person_service: PersonService = Depends(get_person_service)):
#     persons = person_service.get_all()
#     if not persons:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
#     return persons
