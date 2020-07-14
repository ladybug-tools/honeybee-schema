"""Programtype Schema"""
from pydantic import Field, constr

from .._base import NoExtraBaseModel


class VentilationControlAbridged(NoExtraBaseModel):

    type: constr(regex='^VentilationControlAbridged$') = 'VentilationControlAbridged'

    min_indoor_temperature: float = Field(
        -100,
        ge=-100,
        le=100,
        description='A number for the minimum indoor temperature at which to '
        'ventilate in Celsius. Typically, this variable is used to initiate ventilation.'
    )

    max_indoor_temperature: float = Field(
        100,
        ge=-100,
        le=100,
        description='A number for the maximum indoor temperature at which to '
        'ventilate in Celsius. This can be used to set a maximum temperature at '
        'which point ventilation is stopped and a cooling system is turned on.'
    )

    min_outdoor_temperature: float = Field(
        -100,
        ge=-100,
        le=100,
        description='A number for the minimum outdoor temperature at which to ventilate '
        'in Celsius. This can be used to ensure ventilative cooling does not happen '
        'during the winter even if the Room is above the min_indoor_temperature.'
    )

    max_outdoor_temperature: float = Field(
        100,
        ge=-100,
        le=100,
        description='A number for the maximum indoor temperature at which to ventilate '
        'in Celsius. This can be used to set a limit for when it is considered too hot '
        'outside for ventilative cooling.'
    )

    delta_temperature: float = Field(
        -100,
        ge=-100,
        le=100,
        description='A number for the temperature differential in Celsius between '
        'indoor and outdoor below which ventilation is shut off.  This should usually '
        'be a negative number so that ventilation only occurs when the outdoors is '
        'cooler than the indoors. Positive numbers indicate how much hotter the '
        'outdoors can be than the indoors before ventilation is stopped.'
    )

    schedule: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of the schedule for the ventilation over the course of '
        'the year. Note that this is applied on top of any setpoints. The type of this '
        'schedule should be On/Off and values should be either 0 (no possibility of '
        'ventilation) or 1 (ventilation possible).'
    )


class VentilationOpening(NoExtraBaseModel):

    type: constr(regex='^VentilationOpening$') = 'VentilationOpening'

    fraction_area_operable: float = Field(
        0.5,
        ge=0,
        le=1,
        description='A number for the fraction of the window area that is operable.'
    )

    fraction_height_operable: float = Field(
        1.0,
        ge=0,
        le=1,
        description='A number for the fraction of the distance from the bottom of the '
        'window to the top that is operable.'
    )

    discharge_coefficient: float = Field(
        0.17,
        ge=0,
        le=1,
        description='A number that will be multipled by the area of the window in the '
        'stack (buoyancy-driven) part of the equation to account for additional '
        'friction from window geometry, insect screens, etc. Typical values include '
        '0.17, for unobstructed windows with insect screens and 0.25 for unobstructed '
        'windows without insect screens. This value should be lowered if windows are '
        'of an awning or casement type and not allowed to fully open.'
    )

    wind_cross_vent: bool = Field(
        False,
        description='Boolean to indicate if there is an opening of roughly equal area '
        'on the opposite side of the Room such that wind-driven cross ventilation will '
        'be induced. If False, the assumption is that the operable area is primarily on '
        'one side of the Room and there is no wind-driven ventilation.'
    )
