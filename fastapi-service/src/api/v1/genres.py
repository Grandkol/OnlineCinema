from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from models.genres import BaseGenre, Genre
from services.genre import ElasticServiceGenre, get_genre_service

router = APIRouter()


@router.get("/", response_model=list[BaseGenre])
async def all_genres(
    page_number: Annotated[int, Query(description="Page number", ge=1)] = 1,
    page_size: Annotated[
        int, Query(description="Amount of genres at single page", ge=1)
    ] = 50,
    genre_service: ElasticServiceGenre = Depends(get_genre_service),
):
    """
    Получите все жанры:

    - **id**: id Жанра
    - **name**: Название Жанра
    - **description**: Описание жанра

    """
    genres = await genre_service.get_all(page_size=page_size, page_number=page_number)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genres not found")
    return genres


@router.get("/{genre_id}", response_model=Genre)
async def genre_info(
    genre_id: Annotated[str, Path(description="The ID of the genre to get")],
    genre_service: ElasticServiceGenre = Depends(get_genre_service),
):
    """
    Получите Детальную информацию о конкретном жанре:

    - **id**: id Жанра
    - **name**: Название Жанра
    - **description**: Описание жанра
    - **movies**: Название и id всех фильмов в этом жанре
    """
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre not found")
    return genre
