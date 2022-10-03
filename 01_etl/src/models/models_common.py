from abc import ABC

from orjson import loads as orjson_loads
from pydantic import BaseModel


class _AbstractValidator(ABC):
    pass


class _OrjsonDumps():
    def dumps(self, v, *, default):
        return orjson_dumps(v, default=default).decode()


class ModelValidator(_AbstractValidator, BaseModel):
    class Config:
        json_loads = orjson_loads
        json_dumps = _OrjsonDumps().dumps


if __name__ == '__main__':
    ModelValidator()
