from typing import Optional

from fastapi import Query
from pydantic import BaseModel

PagingIdx = Optional[int]


class Paginator(BaseModel):
    from_init: PagingIdx = Query(0, title='Пагинация "с"',
                                 alias='page[number]')
    to_init: PagingIdx = Query(10, title='Пагинация "количество"',
                               alias='page[size]')
