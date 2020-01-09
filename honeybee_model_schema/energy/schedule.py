"""Schedule Type Limit Schema"""
from pydantic import BaseModel, Schema, validator
from typing import List
from enum import Enum

from ._base import NamedEnergyBaseModel
from ..datetime import Date


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


class ScheduleTypeLimit(NamedEnergyBaseModel):
    """Specifies the data types and limits for values contained in schedules."""

    type: Enum('ScheduleTypeLimit', {'type': 'ScheduleTypeLimit'})

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


class ScheduleDay(NamedEnergyBaseModel):
    """Used to describe the daily schedule for a single simulation day."""
    type: Enum('ScheduleDay', {'type': 'ScheduleDay'})

    values: List[float] = Schema(
        ...,
        description='A list of floats or integers for the values of the schedule. '
            'The length of this list must match the length of the times list.'
    )

    times: List[List[float]] = Schema(
        [0, 0],
        description='A list of lists with each sub-list possesing 2 values for '
            '[hour, minute]. The length of the master list must match the length '
            'of the values list. Each time in the master list represents the time '
            'of day that the corresponding value begins to take effect. For example '
            '[(0,0), (9,0), (17,0)] in combination with the values [0, 1, 0] denotes a '
            'schedule value of 0 from 0:00 to 9:00, a value of 1 from 9:00 to 17:00 '
            'and 0 from 17:00 to the end of the day. Note that this representation '
            'of times as the "time of beginning" is a different convention than '
            'EnergyPlus, which uses "time until".'
    )

    @validator('times', whole=True)
    def check_len_times(cls, v):
        for i in v:
            assert len(i) == 2, \
                'Schedule times must each have two values for [hour, minute].'
        return v
    
    @validator('times', whole=True)
    def check_times_values_match(cls, v, values):
        assert len(v) == len(values['values']), 'Length of schedule times must match ' \
            'the schedule values. {} != {}.'.format(len(v), len(values['values']))
        return v

    interpolate: bool = Schema(
        False,
        description='Boolean to note whether values in between times should be '
            'linearly interpolated or whether successive values should take effect '
            'immediately upon the beginning time corrsponding to them.'
    )


class ScheduleRuleAbridged(BaseModel):
    """Schedule rule including a ScheduleDay and when it should be applied.."""

    type: Enum('ScheduleRuleAbridged', {'type': 'ScheduleRuleAbridged'})

    schedule_day: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='A ScheduleDay object associated with this rule.'
    )

    apply_sunday: bool = Schema(
        False,
        description='Boolean noting whether to apply schedule_day on Sundays.'
    )

    apply_monday: bool = Schema(
        False,
        description='Boolean noting whether to apply schedule_day on Mondays.'
    )

    apply_tuesday: bool = Schema(
        False,
        description='Boolean noting whether to apply schedule_day on Tuesdays.'
    )

    apply_wednesday: bool = Schema(
        False,
        description='Boolean noting whether to apply schedule_day on Wednesdays.'
    )

    apply_thursday: bool = Schema(
        False,
        description='Boolean noting whether to apply schedule_day on Thursdays.'
    )

    apply_friday: bool = Schema(
        False,
        description='Boolean noting whether to apply schedule_day on Fridays.'
    )

    apply_saturday: bool = Schema(
        False,
        description='Boolean noting whether to apply schedule_day on Saturdays.'
    )

    apply_holiday: bool = Schema(
        False,
        description='Boolean noting whether to apply schedule_day on Holidays.'
    )

    start_date: List[float] = Schema(
        [1, 1],
        description='A list of two integers for [month, day], representing the date '
            'for the start of the period over which the schedule_day will be applied.'
    )

    @validator('start_date', whole=True)
    def check_len_start_date(cls, v):
        assert len(v) == 2, 'Schedule Rule start_date must each have two ' \
            'values for [month, day].'
        return v

    end_date: List[float] = Schema(
        [12, 31],
        description='A list of two integers for [month, day], representing the date '
            'for the end of the period over which the schedule_day will be applied.'
    )

    @validator('end_date', whole=True)
    def check_len_end_date(cls, v):
        assert len(v) == 2, 'Schedule Rule end_date must each have two ' \
            'values for [month, day].'
        return v


class ScheduleRulesetAbridged(NamedEnergyBaseModel):
    """Used to define a schedule for a default day, further described by ScheduleRule."""

    type: Enum('ScheduleRulesetAbridged', {'type': 'ScheduleRulesetAbridged'})

    day_schedules: List[ScheduleDay]

    default_day_schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='A name for the ScheduleDay that will be used for all days when '
            'no ScheduleRule is applied. This ScheduleDay must be in the day_schedules.'
    )

    schedule_rules: List[ScheduleRuleAbridged] = Schema(
        default=None,
        description='A list of ScheduleRuleAbridged that note exceptions to the '
            'default_day_schedule. These rules should be ordered from highest to '
            'lowest priority.'
    )

    summer_designday_schedule: str = Schema(
        default=None,
        min_length=1,
        max_length=100,
        description='A name for the ScheduleDay that will be used for the summer design '
            'day. This ScheduleDay must be in the day_schedules.'
    )

    winter_designday_schedule: str = Schema(
        default=None,
        min_length=1,
        max_length=100,
        description='A name for the ScheduleDay that will be used for the winter design '
            'day. This ScheduleDay must be in the day_schedules.'
    )

    schedule_type_limit: str = Schema(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of a ScheduleTypeLimit that will be used to validate '
            'schedule values against upper/lower limits and assign units to the '
            'schedule values. If None, no validation will occur.'
    )


class ScheduleFixedIntervalAbridged(NamedEnergyBaseModel):
    """Used to specify a start date and a list of values for a period of analysis."""

    type: Enum('ScheduleFixedIntervalAbridged', {
               'type': 'ScheduleFixedIntervalAbridged'})

    values: List[float] = Schema(
        ...,
        minItems=24,
        maxItems=527040,
        multiple_of=24,
        description='A list of timeseries values occuring at each timestep over '
            'the course of the simulation.'
    )

    schedule_type_limit: str = Schema(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of a ScheduleTypeLimit that will be used to validate '
            'schedule values against upper/lower limits and assign units to the '
            'schedule values. If None, no validation will occur.'
    )

    timestep: int = Schema(
        1,
        description='An integer for the number of steps per hour that the input '
            'values correspond to.  For example, if each value represents 30 '
            'minutes, the timestep is 2. For 15 minutes, it is 4.'
    )

    start_date: Date = Schema(
        None,
        description='Date to note when the input values begin to take effect. If None, '
            'the start date will be [1 Jan].'
    )

    placeholder_value: float = Schema(
        0,
        description=' A value that will be used for all times not covered by the '
            'input values. Typically, your simulation should not need to use this '
            'value if the input values completely cover the simulation period.'
    )

    interpolate: bool = Schema(
        False,
        description='Boolean to note whether values in between intervals should be '
            'linearly interpolated or whether successive values should take effect '
            'immediately upon the beginning time corrsponding to them.'
    )

    @validator('start_date', whole=True)
    def check_range(cls, v, values):
        "Ensure a correct number of schedule values."
        valid_timesteps = (1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60)
        assert values['timestep'] in valid_timesteps, '"{}" is not a valid timestep. ' \
            'Choose from {}'.format(values['timestep'], valid_timesteps)

        if len(values['values']) < 24 * values['timestep']:
             raise ValueError('Number of schedule values must be for at least one day, '
                              'with a length greater than 24 * timestep.')
        max_l = values['timestep'] * 8760 if v is None or not v.is_leap_year \
            else values['timestep'] * 8784
        if len(values['values']) > max_l:
             raise ValueError('Number of schedule values must not exceed a full year, '
                              'with a length greater than 8760 * timestep.')
        if len(values['values']) % (24 * values['timestep']) != 0:
            raise ValueError(
                'Number of schedule values must be for a whole number of days.')
        return v


if __name__ == '__main__':
    print(ScheduleFixedIntervalAbridged.schema_json(indent=2))
    print(ScheduleRulesetAbridged.schema_json(indent=2))
