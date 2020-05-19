"""Wea Schema"""
from pydantic import Field, constr, confloat
from typing import List
import datetime

from .._base import NoExtraBaseModel


class Location(NoExtraBaseModel):
    """Used to specify latitude and longitude of a location on the Earth."""

    type: constr(regex='^Location$') = 'Location'

    latitude: float = Field(
        ...,
        ge=-90,
        le=90,
        description='Location latitude between -90 and 90.'
    )

    longitude: float = Field(
        ...,
        ge=-180,
        le=180,
        description='Location longitude between -180 (west) and 180 (east).'
    )

    time_zone: float = Field(
        default=None,
        ge=-12,
        le=14,
        description='Time zone between -12 hours (west) and +14 hours (east). '
        'If None, the time zone will be an estimated integer value derived from '
        'the longitude in accordance with solar time.'
    )

    elevation: float = Field(
        default=0,
        description='A number for elevation of the location in meters.'
    )

    city: str = Field(
        default='-',
        description='Name of the city as a string.'
    )

    state: str = Field(
        default='-',
        description='Optional state in which the city is located.'
    )

    country: str = Field(
        default='-',
        description='Name of the country as a string.'
    )

    station_id: str = Field(
            default=None,
            description='Optional ID of the location if the location is '
            'representing a weather station.'
        )

    source: str = Field(
            default=None,
            description='Optional source of data (e.g. TMY, TMY3).'
        )


class Wea(NoExtraBaseModel):
    """Used to represent the contents of a Wea file."""

    type: constr(regex='^Wea$') = 'Wea'

    location: Location = Field(
        ...,
        description='Location object to note latitude, longitude and time zone.'
    )

    direct_normal_irradiance: List[confloat(ge=0)] = Field(
        ...,
        description='A list of numbers for the annual direct normal irradiance '
        'in W/m2.'
    )

    diffuse_horizontal_irradiance: List[confloat(ge=0)] = Field(
        ...,
        description='A list of numbers for the annual diffuse horizontal irradiance '
        'in W/m2.'
    )

    timestep: int = Field(
        1,
        ge=0,
        description='An integer to set the number of time steps per hour.'
    )

    is_leap_year: bool = Field(
        False,
        description='A boolean to indicate if values are representing a leap year.'
    )
