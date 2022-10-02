from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, add_pagination, paginate

from .messages import GENRE_NOT_FOUND
from models.genres import Genres
from models.models_common import ModelValidator
from .paginator import Paginator
from services.genres import GenreService, get_genre_service

router = APIRouter()

SearchStr = Optional[str]


@router.get('/{genre_id}',
            response_model=Genres,
            summary='поиск жанра кинопроизведения',
            description='Поиск жанра кинопроизведения по UUID(id)',
            tags=['search by id'])

async def genre_details(genre_id: UUID,
                       genre_service: GenreService = Depends(get_genre_service)) -> ModelValidator:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND)

    return Genres(id=genre.id, name=genre.name)


@router.get('/',
            response_model=Page[Genres],
            summary='поиск жанров кинопроизведений',
            description='полнотекстовый поиск жанров кинопроизведений',
            response_description='список жанров атрибутов кинопроизведений, Dict',
            tags=['FTS'])

async def genres_all(genre_service: GenreService = Depends(get_genre_service),
                    pagination: Paginator = Depends(),
                    query_init: SearchStr = Query(None, title='Строка поиска', alias='query'),
                    ) -> List[Genres]:

    search_params = {'from': pagination.from_init,
                     'size': pagination.to_init,
                     'query': query_init}
    search_fields_with_weigth = {'name': 5}

    genres = await genre_service.get_all(search_params=search_params,
                                             search_fields=search_fields_with_weigth)

    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND)

    return paginate(genres)


add_pagination(router)
