"""Base class for all objects requiring a valid names for all engines."""
from pydantic import BaseModel, Field


class NamedBaseModel(BaseModel):
    """Base class for all objects requiring a valid names for all engines."""

    name: str = Field(
        ...,
        regex=r'[A-Za-z0-9_-]',
        min_length=1,
        max_length=100,
        description='Name of the object used in all simulation engines. Must not '
            'contain spaces and use only letters, digits and underscores/dashes. '
            'It cannot be longer than 100 characters.'
    )

    display_name: str = Field(
        default=None,
        description='Display name of the object with no restrictions.'
    )
