from pydantic import StrictStr, UUID4

from .models_common import ModelValidator


class Genres(ModelValidator):
    """es main parser preparing data for further validation."""

    id: UUID4
    name: StrictStr
