from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import Depends

from db.elastic import get_elastic
from models.genres import Genres
from .services_common import CommonService


class GenreService(CommonService):
    elasticsearch_index = 'genres'
    model_validate = Genres


def get_genre_service(es: AsyncElasticsearch = Depends(get_elastic)) -> GenreService:
    return GenreService(es)
