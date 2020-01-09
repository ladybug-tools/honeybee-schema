"""Base class for all objects requiring a valid EnergyPlus name."""
from pydantic import BaseModel, Field, validator


class NamedEnergyBaseModel(BaseModel):
    """Base class for all objects requiring a valid EnergyPlus name."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='Name of the object. Must use only ASCII characters and '
            'exclude (, ; ! \\n \\t). It cannot be longer than 100 characters.'
    )

    @validator('name')
    def check_name(cls, v):
        assert all(ord(i) < 128 for i in v), 'Name contains non ASCII characters.'
        assert all(char not in v for char in (',', ';', '!', '\n', '\t')), \
            'Name contains invalid character for EnergyPlus (, ; ! \\n \\t).'
        return v
