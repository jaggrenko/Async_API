from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import Depends

from db.elastic import get_elastic
from models.films import Movies
from .services_common import CommonService


class FilmService(CommonService):
    elasticsearch_index = 'movies'
    model_validate = Movies


def get_film_service(es: AsyncElasticsearch = Depends(get_elastic)) -> FilmService:
    return FilmService(es)
