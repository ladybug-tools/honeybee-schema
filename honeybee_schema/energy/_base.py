"""Base classs used by various schema objects."""
from pydantic import BaseModel, Field, validator
import datetime


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


class DatedBaseModel(BaseModel):
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
                datetime.date(2016, v[0] , v[1])
            except ValueError:
                raise ValueError('{}/{} is not a valid date.'.format(v[0], v[1]))
        else:
            try:
                datetime.date(2017, v[0] , v[1])
            except ValueError:
                raise ValueError('{}/{} is not a valid date.'.format(v[0], v[1]))
        return v
