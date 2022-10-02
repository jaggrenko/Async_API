from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, add_pagination, paginate

from .messages import PERSON_NOT_FOUND
from models.persons import Persons
from models.models_common import ModelValidator
from .paginator import Paginator
from services.persons import PersonService, get_person_service

router = APIRouter()

SearchStr = Optional[str]


@router.get('/{person_id}',
            response_model=Persons,
            summary='поиск персоны',
            description='поиск персоны кинопроизведения по UUID(id)',
            tags=['search by id'])
async def person_details(person_id: UUID,
                         person_service: PersonService = Depends(
                             get_person_service)) -> ModelValidator:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=PERSON_NOT_FOUND)

    return person


@router.get('/',
            response_model=Page[Persons],
            summary='поиск персон',
            description='полнотекстовый поиск персон кинопроизведений',
            response_description='список атрибутов персон, Dict',
            tags=['FTS'])
async def persons_all(
        person_service: PersonService = Depends(get_person_service),
        pagination: Paginator = Depends(),
        query_init: SearchStr = Query(None, title='Строка поиска',
                                      alias='query'),
        ) -> List[Persons]:
    search_params = {'from': pagination.from_init,
                     'size': pagination.to_init,
                     'query': query_init}
    search_fields_with_weigth = {'title': 5, 'actors': 3, 'description': 1}

    persons = await person_service.get_all(search_params=search_params,
                                           search_fields=search_fields_with_weigth)

    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=PERSON_NOT_FOUND)

    return paginate(persons)


add_pagination(router)
