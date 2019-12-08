"""Schedule Type Limit Schema"""
from pydantic import BaseModel, Schema, validator
from enum import Enum


class ScheduleNumericType (str, Enum):
    """Designates how the range values are validated."""
    continuous = 'Continuous'
    discrete = 'Discrete'


class ScheduleUnitType (str, Enum):
    dimensionless = 'Dimensionless'
    temperature = 'Temperature'
    delta_temperature = 'DeltaTemperature'
    precipitation_rate = 'PrecipitationRate'
    angle = 'Angle'
    convection_coefficient = 'ConvectionCoefficient'
    activity_level = 'ActivityLevel'
    velocity = 'Velocity'
    capacity = 'Capacity'
    power = 'Power'
    availability = 'Availability'
    percent = 'Percent'
    control = 'Control'
    mode = 'Mode'


class ScheduleTypeLimit(BaseModel):
    """Specifies the data types and limits for values contained in schedules."""

    type: Enum('ScheduleTypeLimit', {'type': 'ScheduleTypeLimit'})

    name: str = Schema(
        ...,
        min_length=1,
        max_length=100
    )

    @validator('name')
    def check_name(cls, v):
        assert all(ord(i) < 128 for i in v), 'Name contains non ASCII characters.'
        assert all(char not in v for char in (',', ';', '!', '\n', '\t')), \
            'Name contains invalid character for EnergyPlus (, ; ! \n \t).'
        assert len(v) > 0, 'Name is an empty string.'
        assert len(v) <= 100, 'Number of characters must be less than 100.'

    lower_limit: float = Schema(
        default=None,
        description='Lower limit for the schedule type is entered.'
    )

    upper_limit: float = Schema(
        default=None,
        description='Upper limit for the schedule type is entered.'
    )

    numeric_type: ScheduleNumericType = ScheduleNumericType.continuous

    unit_type: ScheduleUnitType = ScheduleUnitType.dimensionless
