"""Schedule Ruleset Schema"""
from pydantic import BaseModel, Schema, validator
from typing import List
from enum import Enum


class ScheduleDay(BaseModel):
    """Used to describe the daily schedule for a single simulation day."""
    type: Enum('ScheduleDay', {'type': 'ScheduleDay'})

    name: str = Schema(
        ...,
        min_length=1,
        max_length=100
    )

    @validator('name')
    def check_name_schedule_day(cls, v):
        assert all(ord(i) < 128 for i in v), 'Name contains non ASCII characters.'
        assert all(char not in v for char in (',', ';', '!', '\n', '\t')), \
            'Name contains invalid character for EnergyPlus (, ; ! \n \t).'
        assert len(v) > 0, 'Name is an empty string.'
        assert len(v) <= 100, 'Number of characters must be less than 100.'

    values: List[float]

    times: List[List[float]]

    @validator('times', whole=True)
    def check_len_times(cls, v):
        for i in v:
            if len(i) != 2:
                raise ValueError(
                    'Incorrect number of values.'
                )

    interpolate: bool = Schema(
        False
    )


class ScheduleRuleAbridged(BaseModel):
    """A set of rules assigned to schedule ruleset for specific periods of time and for
  particular days of the week according to a priority sequence."""

    type: Enum('ScheduleRuleAbridged', {'type': 'ScheduleRuleAbridged'})

    schedule_day: str = Schema(
        ...,
        min_length=1,
        max_length=100
    )

    apply_sunday: bool = Schema(
        False
    )

    apply_monday: bool = Schema(
        False
    )

    apply_tuesday: bool = Schema(
        False
    )

    apply_wednesday: bool = Schema(
        False
    )

    apply_thursday: bool = Schema(
        False
    )

    apply_friday: bool = Schema(
        False
    )

    apply_saturday: bool = Schema(
        False
    )

    apply_holiday: bool = Schema(
        False
    )

    start_date: List[float] = Schema(
        [1, 1]
    )

    @validator('start_date', whole=True)
    def check_len_start_date(cls, v):
        if len(v) != 2:
            raise ValueError(
                'Incorrect number of values.'
            )

    end_date: List[float] = Schema(
        [12, 31]
    )

    @validator('end_date', whole=True)
    def check_len_end_date(cls, v):
        if len(v) != 2:
            raise ValueError(
                'Incorrect number of values.'
            )


class ScheduleRulesetAbridged(BaseModel):
    """Used to define a schedule for a default day, further described by ScheduleRule."""

    type: Enum('ScheduleRulesetAbridged', {'type': 'ScheduleRulesetAbridged'})

    name: str = Schema(
        ...,
        min_length=1,
        max_length=100
    )

    @validator('name')
    def check_name_schedule_ruleset(cls, v):
        assert all(ord(i) < 128 for i in v), 'Name contains non ASCII characters.'
        assert all(char not in v for char in (',', ';', '!', '\n', '\t')), \
            'Name contains invalid character for EnergyPlus (, ; ! \n \t).'
        assert len(v) > 0, 'Name is an empty string.'
        assert len(v) <= 100, 'Number of characters must be less than 100.'

    day_schedules: List[ScheduleDay]

    default_day_schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100
    )

    schedule_rules: List[ScheduleRuleAbridged] = Schema(
        default=None
    )

    summer_designday_schedule: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    winter_designday_schedule: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    schedule_type_limit: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )


if __name__ == '__main__':
    print(ScheduleRulesetAbridged.schema_json(indent=2))
