"""DateTime Schema"""
from pydantic import BaseModel, Field, validator
from typing import List, Union
from enum import Enum
from uuid import UUID, uuid4
import datetime


class Date(BaseModel):
    """Date."""

    month: int = Field(
        1,
        ge=1,
        le=12,
        description='An integer for the month between [1-12]. Default is 1.'
    )

    day: int = Field(
        1,
        ge=1,
        le=31,
        description='An integer for day of the month [1-31]. Default is 1.'
    )

    is_leap_year: bool = Field(
        False,
        description='Optional boolean to note whether the date is for a leap year.'
    )

    @validator('is_leap_year')
    def check_date(cls, v, values):
        "Ensure valid start date in case of leap year."
        if v:
            try:
                datetime.date(2016, values['month'] , values['day'])
            except ValueError:
                raise ValueError(
                    '{}/{} is not a valid date.'.format(values['month'], values['day']))
        else:
            try:
                datetime.date(2017, values['month'], values['day'])
            except ValueError:
                raise ValueError(
                    '{}/{} is not a valid date.'.format(values['month'], values['day']))


class Time(BaseModel):
    """Time."""

    hour: int = Field(
        0,
        ge=0,
        le=23,
        description='An integer for the hour between [0-23]. Default is 0.'
    )

    minute: int = Field(
        0,
        ge=0,
        le=59,
        description='An integer for minutes between [0-59]. Default is 0.'
    )
