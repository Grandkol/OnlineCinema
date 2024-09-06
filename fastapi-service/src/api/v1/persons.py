from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from models.film import Film
from models.person import Person
from services.person import PersonService, get_person_service



router = APIRouter()

@router.get('/search', response_model=list[Person])
async def person_search(query: str = '', 
                        page_number: int = 1, 
                        page_size: int = 50,
                        person_service: PersonService = Depends(get_person_service)):
    persons = await person_service.search_person(query, page_number, page_size )
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Persons not found')
    return persons


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)):
    person = await person_service.get_by_id(person_id=person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Person not found')
    return Person(id=person.id, full_name=person.full_name, films=person.films)

@router.get('/{person_id}/film', response_model=list[Film])
async def person_films(person_id: str, person_service: PersonService = Depends(get_person_service)):
    films = await person_service.get_movie_by_person(person_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Films for person not found')
    return films

@router.get('/', response_model=list[Person])
async def all_persons(page_number: int = 1, 
                        page_size: int = 50,
                        person_service: PersonService = Depends(get_person_service)):
    persons = await person_service.get_all(page_size=int(page_size), page_number=int(page_number))
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Persons not found')
    return persons