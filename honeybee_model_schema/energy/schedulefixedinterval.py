"""Schedule Fixed Interval Schema"""
from pydantic import BaseModel, Schema, validator
from typing import List
from enum import Enum
from ..datetime import Date


class ScheduleFixedIntervalAbridged(BaseModel):
    """Used to specify a start date and a list of values for a period of analysis."""

    type: Enum('ScheduleFixedIntervalAbridged', {
               'type': 'ScheduleFixedIntervalAbridged'})

    name: str = Schema(
        ...,
        min_length=1,
        max_length=100
    )

    @validator('name')
    def check_name(cls, v):
        assert all(ord(i) < 128 for i in v), 'Name contains non ASCII characters.'
        assert all(char not in v for char in (',',';','!','\n','\t')), \
            'Name contains invalid character for EnergyPlus (, ; ! \n \t).'
        assert len(v) > 0, 'Name is an empty string.'
        assert len(v) <=100, 'Number of characters must be less than 100.'

    schedule_type_limit: str = Schema(
        default=None
    )

    timestep: float = Schema(
        1
    )

    interpolate: bool = Schema(
        False
    )


    start_date: Date

    values: List[float] = Schema(
        ...,
        minItems=24,
        maxItems=8784,
        description='A list of hourly values for the simulation.'
    )

    @validator('values', whole=True)
    def check_range(cls, v, values):
        "Ensure correct number of values."
        if values['start_date'].is_leap_year == False and len(v) < 24 or len(v) > 8760:
            raise ValueError(
        'Number of values can not be lesser than 24 or greater than 8760 for non-leap year')
        elif values['start_date'].is_leap_year == True and len(v) < 24 or len(v) > 8784: 
            raise ValueError(
        'Number of values can not be lesser than 24 or greater than 8784 for leap year')

    placeholder_value = float

if __name__ == '__main__':
    print(ScheduleFixedIntervalAbridged.schema_json(indent=2))
 