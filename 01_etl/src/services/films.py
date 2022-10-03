from fastapi import Depends

from db.elastic import get_elastic
from models.films import Movies
from .services_common import AbstractService, ElasticsearchService


class FilmService(ElasticsearchService):
    elasticsearch_index = 'movies'
    model_validate = Movies


def get_film_service(es: AbstractService = Depends(get_elastic)) -> FilmService:
    return FilmService(es)
