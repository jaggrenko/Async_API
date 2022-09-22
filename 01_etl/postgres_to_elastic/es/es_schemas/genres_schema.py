import typing

from .common_idx_body import COMMON_IDX_BODY

GENRES_IDX_BODY: typing.Dict = {
    **COMMON_IDX_BODY,
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {
                "type": "keyword"
            },
            "name": {
                "type": "text",
                "analyzer": "ru_en",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
        }
    },
}
