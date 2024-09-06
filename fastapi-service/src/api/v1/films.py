from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from models.film import Film, FilmList
from typing import List,Dict, Union

from services.film import FilmService, get_film_service


router = APIRouter()


@router.get('/search', response_model=List[FilmList])
async def film_detail_list(film_service: FilmService = Depends(get_film_service),
                           query: Union[str, None] = None,
                           page_size: Union[int, None] = 50,
                           page_number: Union[int, None] = 1,
                           sort: Union[str, None] = None,
                           genre: Union[str, None] = None,
                           ) -> List[Film]:

    list = await film_service.get_film_list(sort=sort,
                                            genre=genre,
                                            page_size=page_size,
                                            page_number=page_number,
                                            query=query)
    if not list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return list


@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return film
