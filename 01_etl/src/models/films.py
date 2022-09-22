from typing import List, Optional

from pydantic import StrictStr, StrictFloat, UUID4

from .models_common import ModelValidator


class PersonInFilmByID(ModelValidator):
    """es input parser for custom person aggregation."""

    id: UUID4
    name: StrictStr


class Movies(ModelValidator):
    """es main parser preparing data for further validation."""

    id: UUID4
    imdb_rating: Optional[StrictFloat]
    genre: Optional[List[StrictStr]]
    title: StrictStr
    description: Optional[StrictStr]
    director: Optional[List[StrictStr]]
    actors_names: Optional[List[StrictStr]]
    writers_names: Optional[List[StrictStr]]
    actors: Optional[List[PersonInFilmByID]]
    writers: Optional[List[PersonInFilmByID]]
