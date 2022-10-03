from fastapi import Depends

from db.elastic import get_elastic
from models.persons import Persons
from .services_common import AbstractService, ElasticsearchService


class PersonService(ElasticsearchService):
    elasticsearch_index = 'persons'
    model_validate = Persons


def get_person_service(es: AbstractService = Depends(get_elastic)) -> PersonService:
    return PersonService(es)
