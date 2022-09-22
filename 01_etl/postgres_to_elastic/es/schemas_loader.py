import os
import sys
import typing

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from dotenv import load_dotenv

from es.es_schemas.genres_schema import GENRES_IDX_BODY
from es.es_schemas.movies_schema import MOVIES_IDX_BODY
from es.es_schemas.persons_schema import PERSONS_IDX_BODY

from common.utils.config_validator import ConnectorType, ElasticDSL
from common.utils.db_connectors import ConnectorFactory


def _load_indices(connector: ConnectorFactory,
                  indices: typing.Dict[str, dict], **dsl) -> None:
    with connector_es(**dsl_es) as es:

        for idx, body in indices.items():
            if not es.indices.exists(idx):
                es.indices.create(index=idx, body=body)


if __name__ == '__main__':
    load_dotenv()

    indices = {'genres': GENRES_IDX_BODY,
               'movies': MOVIES_IDX_BODY,
               'persons': PERSONS_IDX_BODY}

    connector_type = ConnectorType()
    connector_es = ConnectorFactory.connect_to(connector_type.connector_es)

    dsl_es = ElasticDSL().dict()
    dsl_es['host'] = '127.0.0.1'

    _load_indices(indices=indices, connector=connector_es, **dsl_es)
