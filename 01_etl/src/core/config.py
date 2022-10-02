import os

from logging import config as logging_config

from pydantic import BaseSettings, Field, StrictStr, StrictInt

from core.logger import LOGGING


class SettingsAPI(BaseSettings):
    """api settings format validation."""

    PROJECT_NAME: StrictStr = Field('movies', env='PROJECT_NAME')

    REDIS_HOST: StrictStr = Field('redis', env='REDIS_HOST')
    REDIS_PORT: StrictInt = Field(6379, env='REDIS_PORT')
    REDIS_CACHE_EXPIRE_IN_SECONDS: StrictInt = 60 * 5

    ELASTIC_HOST: StrictStr = Field('es', env='ELASTIC_HOST')
    ELASTIC_PORT: StrictInt = Field(9200, env='ELASTIC_PORT')

    class Config:
        env_file = '.env'


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__=='__main__':
    logging_config.dictConfig(LOGGING)
    SettingsAPI()
