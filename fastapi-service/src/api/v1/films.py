from http import HTTPStatus
from typing import Dict, List, Union

from fastapi import APIRouter, Depends, HTTPException
from models.film import Film, FilmList
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get("/search", response_model=List[FilmList], tags=["all_films"])
async def film_detail_list(
    film_service: FilmService = Depends(get_film_service),
    query: Union[str, None] = None,
    page_size: Union[int, None] = 50,
    page_number: Union[int, None] = 1,
    sort: Union[str, None] = None,
    genre: Union[str, None] = None,
) -> List[Film]:
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

    list = await film_service.get_film_list(
        sort=sort,
        genre=genre,
        page_size=page_size,
        page_number=page_number,
        query=query,
    )
    if not list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="films not found")

    return list


@router.get("/{film_id}", response_model=Film, tags=["film_detail"])
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
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
