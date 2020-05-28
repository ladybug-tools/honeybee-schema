"""Base class used by various schema objects."""
from pydantic import Field, validator
import datetime

from .._base import NoExtraBaseModel


class IDdEnergyBaseModel(NoExtraBaseModel):
    """Base class for all objects requiring a valid EnergyPlus identifier."""

    identifier: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='Text string for a unique object ID. This identifier remains '
        'constant as the object is mutated, copied, and serialized to different '
        'formats (eg. dict, idf, osm). This identifier is also used to reference '
        'the object across a Model. It must be < 100 characters, use only '
        'ASCII characters and exclude (, ; ! \\n \\t).'
    )

    @validator('identifier')
    def check_identifier(cls, v):
        assert all(ord(i) < 128 for i in v), 'Identifier contains non ASCII characters.'
        assert all(char not in v for char in (',', ';', '!', '\n', '\t')), \
            'Identifier contains an invalid character for EnergyPlus (, ; ! \\n \\t).'
        return v

    display_name: str = Field(
        default=None,
        description='Display name of the object with no character restrictions.'
    )


class DatedBaseModel(NoExtraBaseModel):
    """Base class for all objects needing to check for a valid Date."""

    @staticmethod
    def check_date(v, leap_pear_override=None):
        """Ensure valid date.

        Args:
            v: The Date array to be validated.
            leap_pear_override: Boolean to override the typical check for
                leap year serialization of date arrays. If not None, this
                boolean wil dictate whether the date is a leap year or not.
        """
        if (len(v) == 3 and v[2]) or leap_pear_override:
            try:
                datetime.date(2016, v[0], v[1])
            except ValueError:
                raise ValueError('{}/{} is not a valid date.'.format(v[0], v[1]))
        else:
            try:
                datetime.date(2017, v[0], v[1])
            except ValueError:
                raise ValueError('{}/{} is not a valid date.'.format(v[0], v[1]))
        return v
