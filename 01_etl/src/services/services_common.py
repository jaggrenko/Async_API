from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List, Optional, AnyStr
from uuid import UUID

import backoff
from elasticsearch import AsyncElasticsearch, exceptions
from pydantic import parse_obj_as

from models.models_common import ModelValidator


class AbstractService(ABC):

    @abstractmethod
    def get_by_id(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_all(self, *args, **kwargs):
        pass


class ElasticsearchService(AbstractService):

    def __init__(self, es: AsyncElasticsearch):
        self.es = es

    @property
    @abstractmethod
    def elasticsearch_index(self) -> AnyStr:
        pass

    @staticmethod
    @abstractmethod
    def model_validate(*args, **kwargs) -> ModelValidator:
        pass

    @backoff.on_exception(backoff.expo,
                          (exceptions.ConnectionError,),
                          max_time=10)
    async def get_by_id(self, item_id: UUID) -> Optional[ModelValidator]:
        try:
            docs = await self.es.get(self.elasticsearch_index, item_id)
        except exceptions.NotFoundError:
            return
        return self.model_validate(**docs['_source'])

    @backoff.on_exception(backoff.expo,
                          (exceptions.ConnectionError,),
                          max_time=10)
    async def get_all(self, search_params: Optional[Dict],
                      search_fields: Optional[Dict]) -> List[ModelValidator]:

        body = defaultdict(lambda: defaultdict(dict))
        body.update({'from': search_params.get('from')})
        body.update({'size': search_params.get('size')})

        query = search_params.get('query')

        if query:
            body['query']['bool']['should'] = []

            for field, weight in search_fields.items():
                match = defaultdict(lambda: defaultdict(dict))
                match['match'][field]['query'] = query
                match['match'][field]['boost'] = weight
                body['query']['bool']['should'].append(match)

        else:
            body['query']['match_all'] = {}

        docs = await self.es.search(index=self.elasticsearch_index,
                                    body=body)

        data = map(
            lambda item: {'id': item['_id'], **item['_source']},
            docs.get('hits', dict()).get('hits', list())
        )

        return parse_obj_as(list[self.model_validate], list(data))
