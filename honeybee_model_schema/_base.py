"""Base class for all objects requiring a valid EnergyPlus name."""
from pydantic import BaseModel, Schema, validator


class NamedBaseModel(BaseModel):
    """Base class for all objects requiring a valid names for all engines."""

    name: str = Schema(
        ...,
        regex=r'[A-Za-z0-9_-]',
        min_length=1,
        max_length=100,
        description='Name of the object used in all simulation engines. Must not '
            'contain spaces, use only letters, digits and underscores, and not be '
            'more than 100 characters.'
    )

    display_name: str = Schema(
        default=None,
        description='Display name of the object with no character restrictions.'
    )
