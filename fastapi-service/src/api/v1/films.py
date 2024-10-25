from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from models.film import Film, FilmList
from services.film import ElasticServiceFilm, get_film_service

router = APIRouter()


@router.get("/search", response_model=list[FilmList])
async def film_detail_list(
    film_service: ElasticServiceFilm = Depends(get_film_service),
    query: Annotated[
        str | None, Query(description="Query to find films")
    ] = None,
    page_size: Annotated[
        int, Query(description="Amount of films at single page", ge=1)
    ] = 50,
    page_number: Annotated[int, Query(description="Page number", ge=1)] = 1,
    sort: Annotated[str, Query(description="Field to sort")] = None,
    genre: Annotated[
        str, Query(description="Genre where search movies")
    ] = None,
) -> list[Film]:
    """
    Получите список всех фильмов кинотеатра:

    - **id**: id Кинопроизведения
    - **title**: Название Кинопроизведения
    - **imdb_rating**: Рейтинг Кинопроизведения на imdb
    - **description**: Описание Кинопроизведения
    - **genres**: Список жанров, относящихся к Кинопроизведению
    - **actors**: Актеры Кинопроизведения
    - **writers**: Сцениристы Кинопроизведения
    - **directors**: Режисеры Кинопроизведения

    """

    films = await film_service.get_film_list(
        sort=sort,
        genre=genre,
        page_size=page_size,
        page_number=page_number,
        query=query,
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="films not found")
    return films


@router.get("/{film_id}", response_model=Film)
async def film_details(
    film_id: Annotated[str, Path(description="The ID of the film to get")],
    film_service: ElasticServiceFilm = Depends(get_film_service),
) -> Film:
    """
    Получите детальное описание конкретного Кинофильма:

    - **id**: id Кинопроизведения
    - **title**: Название Кинопроизведения
    - **imdb_rating**: Рейтинг Кинопроизведения на imdb

    """

    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return film
