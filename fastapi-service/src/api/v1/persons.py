from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from models.film import FilmList
from models.person import Person
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get("/search", response_model=list[Person])
async def person_search(
    query: Annotated[
        str | None, Query(description="Query to find persons", max_length=50)
    ] = None,
    page_size: Annotated[
        int, Query(description="Amount of persons at single page", ge=1)
    ] = 50,
    page_number: Annotated[int, Query(description="Page number", ge=1)] = 1,
    person_service: PersonService = Depends(get_person_service),
):
    """
    Получите человка по его имени.

    - **id**: id человека
    - **full_name**: Полное Имя человека
    - **films**: Фильмы, в съемках которых данный человек принимал участие, а также его роль

    """
    persons = await person_service.search_person(query, page_number, page_size)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Persons not found"
        )
    return persons


@router.get("/{person_id}", response_model=Person, tags=["person_detail"])
async def person_details(
    person_id: Annotated[str, Path(description="The ID of the person to get")],
    person_service: PersonService = Depends(get_person_service),
):
    """
    Получите всю информацию о человеке по его id

    - **id**: id человека
    - **full_name**: Полное Имя человека
    - **films**: Фильмы, в съемках которых данный человек принимал участие, а также его роль

    """
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")
    return Person(id=person.id, full_name=person.full_name, films=person.films)


@router.get(
    "/{person_id}/film", response_model=list[FilmList], tags=["person_film_detail"]
)
async def person_films(
    person_id: Annotated[str, Path(description="The ID of the person to get")],
    person_service: PersonService = Depends(get_person_service),
):
    """
    Получите список фильмов, в которых снимался этот человек

    - **id**: id Кинопроизведения
    - **title**: Название Кинопроизведения
    - **imdb_rating**: Рейтинг Кинопроизведения на imdb

    """
    films = await person_service.get_movie_by_person(person_id)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Films for person not found"
        )
    return films


@router.get("/", response_model=list[Person], tags=["person_list"])
async def all_persons(
    page_size: Annotated[
        int, Query(description="Amount of persons at single page", ge=1)
    ] = 50,
    page_number: Annotated[int, Query(description="Page number", ge=1)] = 1,
    person_service: PersonService = Depends(get_person_service),
):
    """
    Получите всех людей в базе данных.

    - **id**: id Жанра
    - **full_name**: Полное Имя человека
    - **films**: Фильмы, в съемках которых данный человек принимал участие, а также его роль

    """
    persons = await person_service.get_all(
        page_size=int(page_size), page_number=int(page_number)
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Persons not found"
        )
    return persons
