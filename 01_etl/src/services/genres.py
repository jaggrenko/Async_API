from fastapi import Depends

from db.elastic import get_elastic
from models.genres import Genres
from .services_common import AbstractService, ElasticsearchService


class GenreService(ElasticsearchService):
    elasticsearch_index = 'genres'
    model_validate = Genres


def get_genre_service(es: AbstractService = Depends(get_elastic)) -> GenreService:
    return GenreService(es)
