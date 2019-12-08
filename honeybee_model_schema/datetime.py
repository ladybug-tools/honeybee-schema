"""DateTime Schema"""
from pydantic import BaseModel, Schema, validator, ValidationError, UrlStr, ConstrainedStr
from typing import List, Union
from enum import Enum
from uuid import UUID, uuid4
import datetime


class Date(BaseModel):
    """Date."""

    month: int = Schema(
        1,
        description='A value for month between `1`-`12`. Default is `1`.',
        ge=1,
        le=12
    )

    day: int = Schema(
        1,
        description='A value for day between `1`-`31`. Default is `1`.',
        ge=1,
        le=31
    )

    is_leap_year: bool = Schema(
        False
    )

    @validator('is_leap_year')
    def check_date(cls, v, values):
        "Ensure valid start date in case of leap year."
        if v == True:
            try:
                datetime.date(2016, values['month'] , values['day'])
            except ValueError:
                raise ValueError(
                    '{}/{} is not a valid date.'.format(values['month'], values['day']))
        elif v == False:
            try:
                datetime.date(2017, values['month'], values['day'])
            except ValueError:
                raise ValueError(
                    '{}/{} is not a valid date.'.format(values['month'], values['day']))
        else:
            return v


class Time(BaseModel):
    """Time."""

    hour: int = Schema(
        0,
        description='A value for hour between `0`-`24`. Default is `0`.',
        ge=0,
        le=24
    )

    minute: int = Schema(
        0,
        description='A value for minutes between `0`-`59`. Default is `0`.',
        ge=0,
        le=59
    )

    @validator('minute')
    def check_time(cls, v, values):
        if not 'hour' in values:
            return v
        try:
            datetime.time(values['hour'], v)

        except:
            if values['hour'] == 24 and v == 00:
                return v
            else:
                raise ValueError(
                    '{}:{} is not a valid time.'.format(values['hour'], v))
        else:
            return v
