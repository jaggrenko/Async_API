from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, add_pagination, paginate

from .messages import FILM_NOT_FOUND
from models.films import Movies
from models.models_common import ModelValidator
from services.films import FilmService, get_film_service

router = APIRouter()

PagingIdx = Optional[int]
SearchStr = Optional[str]


@router.get('/{film_id}',
            response_model=Movies,
            summary='поиск кинопроизведения',
            description='Поиск кинопроизведения по UUID(id)',
            tags=['search by id'])

async def film_details(film_id: UUID,
                       film_service: FilmService = Depends(get_film_service)) -> ModelValidator:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)

    return Movies(id=film.id, title=film.title)


@router.get('/',
            response_model=Page[Movies],
            summary='поиск кинопроизведений',
            description='полнотекстовый поиск кинопроизведений',
            response_description='список атрибутов кинопроизведений, Dict',
            tags=['FTS'])

async def films_all(film_service: FilmService = Depends(get_film_service),
                    from_init: PagingIdx = Query(0, title='Пагинация "с"', alias='page[number]'),
                    to_init: PagingIdx = Query(10, title='Пагинация "количество"', alias='page[size]'),
                    query_init: SearchStr = Query(None, title='Строка поиска', alias='query'),
                    ) -> List[Movies]:

    search_params = {'from': from_init, 'size': to_init, 'query': query_init}
    search_fields_with_weigth = {'title': 5, 'actors': 3, 'description': 1}

    films = await film_service.get_all(search_params=search_params,
                                             search_fields=search_fields_with_weigth)

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)

    return paginate(films)


add_pagination(router)
