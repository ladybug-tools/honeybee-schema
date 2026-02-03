"""Base class used by radiance schema objects."""
from pydantic import Field
from typing import Union
from .._base import NoExtraBaseModel


class IDdRadianceBaseModel(NoExtraBaseModel):
    """Base class for all objects requiring a valid Radiance identifier."""

    identifier: str = Field(
        ...,
        pattern=r'^[.A-Za-z0-9_-]+$',
        min_length=1,
        description='Text string for a unique Radiance object. Must not contain spaces '
                    'or special characters. This will be used to identify the object '
                    'across a model and in the exported Radiance files.'
    )

    display_name: Union[str, None] = Field(
        default=None,
        description='Display name of the object with no character restrictions.'
    )
