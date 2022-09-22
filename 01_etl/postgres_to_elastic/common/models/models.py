from abc import ABC
from pydantic import BaseModel, StrictStr, StrictFloat, UUID4, validator
from typing import Iterable, List, Optional


class AbstractValidator(ABC):
    pass


class ModelValidator(AbstractValidator, BaseModel):
    pass


class GenresElastic(ModelValidator):
    """pg input parser model for genres table."""

    name: StrictStr


class PersonInFilm(ModelValidator):
    """pg input parser model for person table."""

    name: StrictStr


class PersonInFilmByID(ModelValidator):
    """pg input parser for custom person aggregation."""

    id: UUID4
    name: StrictStr


class RolesElastic(ModelValidator):
    """pg input parser model for roles table."""

    role: StrictStr


class MoviesElasticID(ModelValidator):
    """pg input parser for custom movies_id aggregation."""

    id: UUID4


class MoviesPG(ModelValidator):
    """pg main parser preparing data for further validation."""

    id: UUID4
    imdb_rating: Optional[StrictFloat]
    genre: Optional[List[GenresElastic]]
    title: Optional[StrictStr]
    description: Optional[StrictStr]
    director: Optional[List[PersonInFilm]]
    actors_names: Optional[List[PersonInFilm]]
    writers_names: Optional[List[PersonInFilm]]
    actors: Optional[List[PersonInFilmByID]]
    writers: Optional[List[PersonInFilmByID]]

    @validator('actors_names', 'writers_names', 'director', 'genre')
    def unpack_field_data(cls, data_packed: Iterable):
        """transform raw data for es field format."""

        if data_packed:
            return [data_to_transform.name for data_to_transform in
                    data_packed]
        return []


class GenresPG(ModelValidator):
    id: UUID4
    name: StrictStr


class PersonsPG(ModelValidator):
    id: UUID4
    name: StrictStr
    roles: Optional[List[RolesElastic]]
    movies_id: Optional[List[MoviesElasticID]]

    @validator('roles')
    def unpack_field_roles(cls, data_packed: Iterable):
        """transform raw data for es field format."""

        if data_packed:
            return [data_to_transform.role for data_to_transform in
                    data_packed]
        return []

    @validator('movies_id')
    def unpack_field_id(cls, data_packed: Iterable):
        """transform raw data for es field format."""

        if data_packed:
            return [data_to_transform.id for data_to_transform in
                    data_packed]
        return []