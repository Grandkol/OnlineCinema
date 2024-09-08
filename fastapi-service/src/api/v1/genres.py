from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from models.film import Film
from models.genres import BaseGenre, Genre
from models.person import Person
from pydantic import BaseModel
from services.genre import GenreService, get_genre_service
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get("/", response_model=list[BaseGenre], tags=["genre_list"])
async def all_genres(
    page_number: int = 1,
    page_size: int = 50,
    genre_service: GenreService = Depends(get_genre_service),
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


@router.get("/{genre_id}", response_model=Genre, tags=["genre_detail"])
async def genre_info(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service)
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
