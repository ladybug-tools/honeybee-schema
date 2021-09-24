"""Schedule Type Limit Schema"""
from pydantic import Field, validator, root_validator, constr, conlist
from typing import List, Union
from enum import Enum
import datetime

from ._base import IDdEnergyBaseModel, DatedBaseModel, EnergyBaseModel
from ..altnumber import NoLimit


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


class ScheduleTypeLimit(EnergyBaseModel):
    """Specifies the data types and limits for values contained in schedules."""

    type: constr(regex='^ScheduleTypeLimit$') = 'ScheduleTypeLimit'

    lower_limit: Union[NoLimit, float] = Field(
        default=NoLimit(),
        description='Lower limit for the schedule type or NoLimit.'
    )

    upper_limit: Union[NoLimit, float] = Field(
        default=NoLimit(),
        description='Upper limit for the schedule type or NoLimit.'
    )

    numeric_type: ScheduleNumericType = ScheduleNumericType.continuous

    unit_type: ScheduleUnitType = ScheduleUnitType.dimensionless


class ScheduleDay(EnergyBaseModel):
    """Used to describe the daily schedule for a single simulation day."""

    type: constr(regex='^ScheduleDay$') = 'ScheduleDay'

    values: List[float] = Field(
        ...,
        description='A list of floats or integers for the values of the schedule. '
        'The length of this list must match the length of the times list.'
    )

    times: List[conlist(int, min_items=2, max_items=2)] = Field(
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

    @root_validator
    def check_times_values_match(cls, values):
        "Ensure the length of the times matches the length of the values."
        times, vals = values.get('times'), values.get('values')
        assert len(times) == len(vals), 'Length of schedule times must match ' \
            'the schedule values. {} != {}.'.format(len(times), len(values['values']))
        return values

    interpolate: bool = Field(
        False,
        description='Boolean to note whether values in between times should be '
        'linearly interpolated or whether successive values should take effect '
        'immediately upon the beginning time corresponding to them.'
    )


class ScheduleRuleAbridged(DatedBaseModel):
    """Schedule rule including a ScheduleDay and when it should be applied.."""

    type: constr(regex='^ScheduleRuleAbridged$') = 'ScheduleRuleAbridged'

    schedule_day: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='The identifier of a ScheduleDay object associated with this rule.'
    )

    apply_sunday: bool = Field(
        False,
        description='Boolean noting whether to apply schedule_day on Sundays.'
    )

    apply_monday: bool = Field(
        False,
        description='Boolean noting whether to apply schedule_day on Mondays.'
    )

    apply_tuesday: bool = Field(
        False,
        description='Boolean noting whether to apply schedule_day on Tuesdays.'
    )

    apply_wednesday: bool = Field(
        False,
        description='Boolean noting whether to apply schedule_day on Wednesdays.'
    )

    apply_thursday: bool = Field(
        False,
        description='Boolean noting whether to apply schedule_day on Thursdays.'
    )

    apply_friday: bool = Field(
        False,
        description='Boolean noting whether to apply schedule_day on Fridays.'
    )

    apply_saturday: bool = Field(
        False,
        description='Boolean noting whether to apply schedule_day on Saturdays.'
    )

    start_date: List[int] = Field(
        [1, 1],
        min_items=2,
        max_items=3,
        description='A list of two integers for [month, day], representing the start '
        'date of the period over which the schedule_day will be applied.'
        'A third integer may be added to denote whether the date should be '
        're-serialized for a leap year (it should be a 1 in this case).'
    )

    @validator('start_date')
    def check_start_date(cls, v):
        return cls.check_date(v)

    end_date: List[int] = Field(
        [12, 31],
        min_items=2,
        max_items=3,
        description='A list of two integers for [month, day], representing the end '
        'date of the period over which the schedule_day will be applied.'
        'A third integer may be added to denote whether the date should be '
        're-serialized for a leap year (it should be a 1 in this case).'
    )

    @validator('end_date')
    def check_end_date(cls, v):
        return cls.check_date(v)


class ScheduleRulesetAbridged(IDdEnergyBaseModel):
    """Used to define a schedule for a default day, further described by ScheduleRule."""

    type: constr(regex='^ScheduleRulesetAbridged$') = 'ScheduleRulesetAbridged'

    day_schedules: List[ScheduleDay] = Field(
        ...,
        description='A list of ScheduleDays that are referenced in the other keys of '
        'this ScheduleRulesetAbridged.'
    )

    default_day_schedule: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='An identifier for the ScheduleDay that will be used for '
        'all days when no ScheduleRule is applied. This ScheduleDay must be '
        'in the day_schedules.'
    )

    schedule_rules: List[ScheduleRuleAbridged] = Field(
        default=None,
        description='A list of ScheduleRuleAbridged that note exceptions to the '
        'default_day_schedule. These rules should be ordered from highest to '
        'lowest priority.'
    )

    holiday_schedule: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='An identifier for the ScheduleDay that will be used for holidays. '
        'This ScheduleDay must be in the day_schedules.'
    )

    summer_designday_schedule: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='An identifier for the ScheduleDay that will be used for '
        'the summer design day. This ScheduleDay must be in the day_schedules.'
    )

    winter_designday_schedule: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='An identifier for the ScheduleDay that will be used for the '
        'winter design day. This ScheduleDay must be in the day_schedules.'
    )

    schedule_type_limit: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of a ScheduleTypeLimit that will be used to validate '
        'schedule values against upper/lower limits and assign units to the '
        'schedule values. If None, no validation will occur.'
    )


class ScheduleRuleset(ScheduleRulesetAbridged):
    """Used to define a schedule for a default day, further described by ScheduleRule."""

    type: constr(regex='^ScheduleRuleset$') = 'ScheduleRuleset'

    schedule_type_limit: ScheduleTypeLimit = Field(
        default=None,
        description='ScheduleTypeLimit object that will be used to validate '
        'schedule values against upper/lower limits and assign units to the '
        'schedule values. If None, no validation will occur.'
    )


class ScheduleFixedIntervalAbridged(IDdEnergyBaseModel):
    """Used to specify a start date and a list of values for a period of analysis."""

    type: constr(regex='^ScheduleFixedIntervalAbridged$') = \
        'ScheduleFixedIntervalAbridged'

    values: List[float] = Field(
        ...,
        min_items=24,
        max_items=527040,
        description='A list of timeseries values occuring at each timestep over '
        'the course of the simulation.'
    )

    schedule_type_limit: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of a ScheduleTypeLimit that will be used to validate '
        'schedule values against upper/lower limits and assign units to the '
        'schedule values. If None, no validation will occur.'
    )

    timestep: int = Field(
        1,
        description='An integer for the number of steps per hour that the input '
        'values correspond to.  For example, if each value represents 30 '
        'minutes, the timestep is 2. For 15 minutes, it is 4.'
    )

    @validator('timestep')
    def check_timestep(cls, v):
        "Ensure the timestep is acceptable by EnergyPlus."
        valid_timesteps = (1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60)
        assert v in valid_timesteps, '"{}" is not a valid timestep. ' \
            'Choose from {}'.format(v, valid_timesteps)
        return v

    start_date: List[int] = Field(
        [1, 1],
        min_items=2,
        max_items=3,
        description='A list of two integers for [month, day], representing the start '
        'date when the schedule values begin to take effect.'
        'A third integer may be added to denote whether the date should be '
        're-serialized for a leap year (it should be a 1 in this case).'
    )

    @validator('start_date')
    def check_start_date(cls, v):
        if len(v) == 3 and v[2]:
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

    placeholder_value: float = Field(
        0,
        description=' A value that will be used for all times not covered by the '
        'input values. Typically, your simulation should not need to use this '
        'value if the input values completely cover the simulation period.'
    )

    interpolate: bool = Field(
        False,
        description='Boolean to note whether values in between intervals should be '
        'linearly interpolated or whether successive values should take effect '
        'immediately upon the beginning time corresponding to them.'
    )

    @root_validator
    def check_number_of_values(cls, values):
        "Ensure an acceptable number of schedule values."
        vals = values.get('values')
        timestep = values.get('timestep')
        start_date = values.get('start_date')
        if len(vals) < 24 * timestep:
            raise ValueError('Number of schedule values must be for at least one day, '
                             'with a length greater than 24 * timestep.')
        max_l = timestep * 8760 if len(start_date) == 3 and start_date[2] \
            else timestep * 8784
        if len(vals) > max_l:
            raise ValueError('Number of schedule values must not exceed a full year, '
                             'with a length greater than 8760 * timestep.')
        if len(vals) % (24 * timestep) != 0:
            raise ValueError(
                'Number of schedule values must be for a whole number of days.')
        return values


class ScheduleFixedInterval(ScheduleFixedIntervalAbridged):
    """Used to specify a start date and a list of values for a period of analysis."""

    type: constr(regex='^ScheduleFixedInterval$') = 'ScheduleFixedInterval'

    schedule_type_limit: ScheduleTypeLimit = Field(
        default=None,
        description='ScheduleTypeLimit object that will be used to validate '
        'schedule values against upper/lower limits and assign units to the '
        'schedule values. If None, no validation will occur.',
    )
