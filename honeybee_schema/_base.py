"""Base class for all objects requiring a valid names for all engines."""
from pydantic import BaseModel, Field, Extra


class NoExtraBaseModel(BaseModel):
    """Base class for all objects that are not extensible with additional keys.

    This effectively includes all objects except for the Properties classes
    that are assigned to geometry objects.
    """

    class Config:
        extra = Extra.forbid


class IDdBaseModel(NoExtraBaseModel):
    """Base class for all objects requiring a identifiers acceptable for all engines."""

    identifier: str = Field(
        ...,
        regex=r'^[.A-Za-z0-9_-]+$',
        min_length=1,
        max_length=100,
        description='Text string for a unique object ID. This identifier remains '
        'constant as the object is mutated, copied, and serialized to different '
        'formats (eg. dict, idf, rad). This identifier is also used to reference '
        'the object across a Model. It must be < 100 characters and not contain '
        'any spaces or special characters.'
    )

    display_name: str = Field(
        default=None,
        description='Display name of the object with no character restrictions.'
    )

    user_data: dict = Field(
        default=None,
        description='Optional dictionary of user data associated with the object.'
        'All keys and values of this dictionary should be of a standard data '
        'type to ensure correct serialization of the object (eg. str, float, '
        'int, list).'
    )
