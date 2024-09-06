from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from models.genres import Genre
from models.film import Film
from models.person import Person
from services.person import PersonService, get_person_service
from services.genre import get_genre_service, GenreService



router = APIRouter()



@router.get('/', response_model=list[Genre])
async def all_genres(page_number: int = 1, 
                    page_size: int = 50,
                    genre_service: GenreService = Depends(get_genre_service)):
    genres = await genre_service.get_all(page_size=page_size, page_number=page_number)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genres not found')
    return genres


@router.get('/{genre_id}', response_model=Genre)
async def genre_info(genre_id: str, genre_service: GenreService = Depends(get_genre_service)):
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre not found')
    return genre
