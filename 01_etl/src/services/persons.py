from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import Depends

from db.elastic import get_elastic
from models.persons import Persons
from .services_common import CommonService


class PersonService(CommonService):
    elasticsearch_index = 'persons'
    model_validate = Persons


def get_person_service(es: AsyncElasticsearch = Depends(get_elastic)) -> PersonService:
    return PersonService(es)
