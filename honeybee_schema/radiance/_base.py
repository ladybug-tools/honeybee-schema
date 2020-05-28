"""Base class used by radiance schema objects."""
from pydantic import Field, validator
import re
from .._base import NoExtraBaseModel


class IDdRadianceBaseModel(NoExtraBaseModel):
    """Base class for all objects requiring a valid Radiance identifier."""

    identifier: str = Field(
        ...,
        description='Text string for a unique Radiance object. Must not contain spaces '
                    'or special characters. This will be used to identify the object '
                    'across a model and in the exported Radiance files.'
    )

    @validator('identifier')
    def valid_rad_string(cls, value):
        """Check that a string is valid for Radiance.

        This method is modified from the honeybee-core.typing.valid_rad_string method.
        """
        try:
            illegal_match = re.search(r'[^.A-Za-z0-9_-]', value)
        except TypeError:
            raise TypeError('Identifier must be a text string. Got {}: {}.'.format(
                type(value), value))
        assert illegal_match is None, \
            'Illegal character "{}" found in identifier'.format(illegal_match.group(0))
        assert len(value) > 0, \
            'Input identifier "{}" contains no characters.'.format(value)
        return value

    display_name: str = Field(
        default=None,
        description='Display name of the object with no character restrictions.'
    )
