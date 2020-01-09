"""Programtype Schema"""
from pydantic import BaseModel, Schema, validator
from typing import Union
from enum import Enum

from ._base import NamedEnergyBaseModel


class PeopleAbridged(NamedEnergyBaseModel):

    type: Enum('PeopleAbridged', {'type': 'PeopleAbridged'})

    people_per_area: float = Schema(
        ...,
        ge=0,
        description='People per floor area expressed as [people/m2]'
    )

    occupancy_schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='Name of a schedule for the occupancy over the course of the '
            'year. The type of this schedule should be Fractional and the fractional '
            'values will get multiplied by the people_per_area to yield a complete '
            'occupancy profile.'
    )

    activity_schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='Name of a schedule for the activity of the occupants over the '
            'course of the year. The type of this schedule should be Power and the '
            'values of the schedule equal to the number of Watts given off by an '
            'individual person in the room.'
    )

    radiant_fraction: float = Schema(
        0.3,
        ge=0,
        le=1,
        description='The radiant fraction of sensible heat released by people. The default'
        'value is 0.30.'
    )

    latent_fraction: Union[float, str] = Schema(
        'autocalculate',
        ge=0,
        le=1,
        description='Number for the latent fraction of heat gain due to people or '
            'simply the word "autocalculate".'
    )

    @validator('latent_fraction')
    def check_string_latent_fraction(cls, v):
        if not isinstance(v, float) and v != 'autocalculate':
            raise ValueError('"{}" is not a valid entry for latent_fraction'.format(v))


class LightingAbridged(NamedEnergyBaseModel):

    type: Enum('LightingAbridged', {'type': 'LightingAbridged'})

    watts_per_area: float = Schema(
        ...,
        ge=0,
        description='Lighting per floor area as [W/m2].'
    )

    schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='Name of the schedule for the use of lights over the course of '
            'the year. The type of this schedule should be Fractional and the '
            'fractional values will get multiplied by the watts_per_area to yield a '
            'complete lighting profile.'
    )

    visible_fraction: float = Schema(
        0.25,
        ge=0,
        le=1,
        description='The fraction of heat from lights that goes into the zone as visible '
        '(short-wave) radiation. The default value is `0.25`.'
    )

    radiant_fraction: float = Schema(
        0.32,
        ge=0,
        le=1,
        description='The fraction of heat from lights that is long-wave radiation. Default'
        ' value is `0.32`.'
    )

    return_air_fraction: float = Schema(
        0.0,
        ge=0,
        le=1,
        description='The fraction of the heat from lights that goes into the zone return '
        'air. Default value is `0`.'
    )

    @validator('return_air_fraction')
    def check_sum(cls, v, values): 
        "Ensure sum is less than 1."
        assert (v + values['visible_fraction'] + values['radiant_fraction']) < 1, \
            'Sum of visible, radiant, and return air fractions cannot be greater than 1.'


class _EquipmentBase(NamedEnergyBaseModel):

    watts_per_area: float = Schema(
        ...,
        ge=0,
        description='Equipment level per floor area as [W/m2].'
    )

    schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='Name of the schedule for the use of equipment over the course '
            'of the year. The type of this schedule should be Fractional and the '
            'fractional values will get multiplied by the watts_per_area to yield '
            'a complete equipment profile.'
    )

    radiant_fraction: float = Schema(
        0,
        ge=0,
        le=1,
        description='Number for the amount of long-wave radiation heat given off'
        ' by electric equipment. Default value is 0.'
    )

    latent_fraction: Union[float, str] = Schema(
        0,
        ge=0,
        le=1,
        description='Number for the amount of latent heat given off by electric' 
        'equipment. Default value is 0.'

    )

    lost_fraction: float = Schema(
        0,
        ge = 0,
        le = 1,
        description='Number for the amount of “lost” heat being given off by '
            'equipment. The default value is 0.'
    )

class ElectricEquipmentAbridged(_EquipmentBase):

    type: Enum('ElectricEquipmentAbridged', {'type': 'ElectricEquipmentAbridged'})


class GasEquipmentAbridged(_EquipmentBase):

    type: Enum('GasEquipmentAbridged', {'type': 'GasEquipmentAbridged'})


class InfiltrationAbridged(NamedEnergyBaseModel):

    type: Enum('InfiltrationAbridged', {'type': 'InfiltrationAbridged'})

    flow_per_exterior_area: float = Schema(
        ...,
        ge=0,
        description='Number for the infiltration per exterior surface area in m3/s-m2.'
    )

    schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='Name of the schedule for the infiltration over the course of '
            'the year. The type of this schedule should be Fractional and the '
            'fractional values will get multiplied by the flow_per_exterior_area '
            'to yield a complete infiltration profile.'
    )

    constant_coefficient: float = Schema(
        1,
        ge=0
    )

    temperature_coefficient: float = Schema(
        0,
        ge=0
    )

    velocity_coefficient: float = Schema(
        0,
        ge=0
    )


class VentilationAbridged(NamedEnergyBaseModel):

    type: Enum('VentilationAbridged', {'type': 'VentilationAbridged'})

    flow_per_person: float = Schema(
        0,
        ge=0,
        description='Intensity of ventilation in[] m3/s per person]. Note that '
            'setting this value does not mean that ventilation is varied based on '
            'real-time occupancy but rather that the design level of ventilation '
            'is determined using this value and the People object of the Room.'
    )

    flow_per_area: float = Schema(
        0,
        ge=0,
        description='Intensity of ventilation in [m3/s per m2 of floor area].'
    )

    air_changes_per_hour: float = Schema(
        0,
        ge = 0,
        description='Intensity of ventilation in air changes per hour (ACH) for '
            'the entire Room.'
    )

    flow_per_zone: float = Schema(
        0,
        ge = 0,
        description='Intensity of ventilation in m3/s for the entire Room.'
    )

    schedule: str = Schema(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of the schedule for the ventilation over the course of '
            'the year. The type of this schedule should be Fractional and the '
            'fractional values will get multiplied by the total design flow rate '
            '(determined from the sum of the other 4 fields) to yield a complete '
            'ventilation profile.'
    )

class SetpointAbridged(NamedEnergyBaseModel):
    """Used to specify information about the setpoint schedule."""

    type: Enum('SetpointAbridged', {'type': 'SetpointAbridged'})   

    cooling_schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='Name of the schedule for the cooling setpoint. The values in '
            'this schedule should be temperature in [C].'
    )

    heating_schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='Name of the schedule for the heating setpoint. The values in '
            'this schedule should be temperature in [C].'
    )

    humidification_schedule: str = Schema(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of the schedule for the humidification setpoint. The values '
            'in this schedule should be in [%].'
    )

    dehumidification_schedule: str = Schema(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of the schedule for the dehumidification setpoint. The values '
            'in this schedule should be in [%].'
    )


if __name__ == '__main__':
    print(PeopleAbridged.schema_json(indent=2))
    print(LightingAbridged.schema_json(indent=2))
    print(ElectricEquipmentAbridged.schema_json(indent=2))
    print(GasEquipmentAbridged.schema_json(indent=2))
    print(InfiltrationAbridged.schema_json(indent=2))
    print(VentilationAbridged.schema_json(indent=2))
    print(SetpointAbridged.schema_json(indent=2))
