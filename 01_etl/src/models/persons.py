from typing import List, Optional

from pydantic import StrictStr, UUID4

from .models_common import ModelValidator


class Persons(ModelValidator):
    """es main parser preparing data for further validation."""

    id: UUID4
    name: StrictStr
    roles: Optional[List[StrictStr]]
    movies_id: Optional[List[UUID4]]
