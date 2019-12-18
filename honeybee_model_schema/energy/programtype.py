"""Programtype Schema"""
from pydantic import BaseModel, Schema, validator
from typing import Union
from enum import Enum


class PeopleAbridged(BaseModel):
    """Used to model the occupant's effect on the space conditions."""

    type: Enum('PeopleAbridged', {'type': 'PeopleAbridged'})

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

    people_per_area: float = Schema(
        ...,
        ge=0,
        description='People per floor area expressed as people/m²'
    )

    radiant_fraction: float = Schema(
        0.3,
        ge=0,
        le=1,
        description='The radiant fraction of sensible heat released by people. The default'
        'value is 0.30.'
    )

    latent_fraction: float = Schema(
        default=None,
        ge=0,
        le=1,
        description='Used to specify a fixed latent fraction of heat gain due to people. \
            If left null then Honeybee will autocalculate this value.'
    )

    occupancy_schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='Used to describe the occupancy schedule for people.'
    )

    activity_schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='Schedule that determines the amount of heat gain per person.'
    )


class LightingAbridged(BaseModel):
    """Used to specify the information about the electric lighting system."""

    type: Enum('LightingAbridged', {'type': 'LightingAbridged'})

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

    watts_per_area: float = Schema(
        ...,
        ge=0,
        description='Lighting per floor area expressed as watts/m².'
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
        0.00,
        ge=0,
        le=1,
        description='The fraction of the heat from lights that goes into the zone return '
        'air. Default value is `0`.'
    )

    @validator('return_air_fraction')
    def check_sum(cls, v, values): 
        "Ensure sum is less than 1."
        if not 'visible_fraction' in values or not 'radiant_fraction' in values:
            return v
        elif (v + values['visible_fraction']+ values['radiant_fraction']) > 1:

            raise ValueError(
        'Sum cannot be greater than 1.')

    schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='Used to describe the schedule for lighting as a fraction applied to '
        'design level of lights.'
    )


class ElectricEquipmentAbridged(BaseModel):
    """Used to specify information about the electrical equipment."""

    type: Enum('ElectricEquipmentAbridged', {'type': 'ElectricEquipmentAbridged'})

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

    watts_per_area: float = Schema(
        ...,
        ge=0,
        description='Equipment level per floor area expressed as watts/m².'
    )

    radiant_fraction: float = Schema(
        0,
        ge=0,
        le=1,
        description='Used to characterise the amount of long-wave radiation heat given off'
        ' by electric equipment. Default value is 0.'
    )

    latent_fraction: float = Schema(
        0,
        ge=0,
        le=1,
        description='Used to characterise the amount of latent heat given off by electric' 
        'equipment. Default value is 0.'

    )

    lost_fraction: float = Schema(
        0,
        ge = 0,
        le = 1,
        description='Used to characterize the amount of “lost” heat being given off by '
        'equipment. The default value is 0.'
    )


    schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='Used to describe the schedule for equipment as a fraction applied to'
        ' design level for electric equipment.'
    )


class GasEquipmentAbridged(BaseModel):
    """Used to specify information about the gas equipment."""

    type: Enum('GasEquipmentAbridged', {'type': 'GasEquipmentAbridged'})

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

    watts_per_area: float = Schema(
        ...,
        ge=0,
        description='Equipment level per floor area expressed as watts/m².'
    )

    radiant_fraction: float = Schema(
        0,
        ge=0,
        le=1,
        description='Used to characterise the amount of long-wave radiation heat given off'
        ' by electric equipment.'
    )

    latent_fraction: float = Schema(
        0,
        ge=0,
        le=1,
        description='Used to characterise the amount of latent heat given off by electric' 
        'equipment. Default value is 0.'

    )

    lost_fraction: float = Schema(
        0,
        ge = 0,
        le = 1,
        description='Used to characterize the amount of “lost” heat being given off by '
        'equipment. The default value is 0.'
    )    

    schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='Used to describe the schedule for equipment as a fraction applied to'
        ' design level for electric equipment.'
    )


class InfiltrationAbridged(BaseModel):
    """Used to model the infiltration of air from the outdoor environment into a thermal zone."""

    type: Enum('InfiltrationAbridged', {'type': 'InfiltrationAbridged'})

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

    flow_per_exterior_area: float = Schema(
        ...,
        ge=0,
        description='Used to model the infiltration per exterior surface area in m3/s-m2.'
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

    schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100,
        description='Used to describe the schedule for equipment as a fraction applied to'
        ' design level for electric equipment.'
    )


class VentilationAbridged(BaseModel):
    """Used to model the purposeful flow of air from the outdoor environment directly into a thermal zone."""

    type: Enum('VentilationAbridged', {'type': 'VentilationAbridged'})

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

    air_changes_per_hour: float = Schema(
        0,
        ge = 0
    )

    flow_per_zone: float = Schema(
        0,
        ge = 0,
        description='Unit is m3/s. Default value is 0.'
    )

    flow_per_person: float = Schema(
        None,
        ge=0,
        description='Used to model the ventilation flow rate per person in m3/s-person.'
    )

    flow_per_area: float = Schema(
        None,
        ge=0,
        description='Used to model the ventilation flow rate per zone floor area in m3/s-m2.'
    )

    schedule: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

class SetpointAbridged(BaseModel):
    """Used to specify information about the setpoint schedule."""

    type: Enum('SetpointAbridged', {'type': 'SetpointAbridged'})   

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

    cooling_schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100
    )

    heating_schedule: str = Schema(
        ...,
        min_length=1,
        max_length=100
    )

    humidification_schedule: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    dehumidification_schedule: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )


class ProgramTypeAbridged(BaseModel):
    """A set of programs."""

    type: Enum('ProgramTypeAbridged', {'type': 'ProgramTypeAbridged'})

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
    
    people: PeopleAbridged = Schema(
        default = None
    )

    lighting: LightingAbridged = Schema(
        default = None
    )

    electrical_equipment: ElectricEquipmentAbridged = Schema(
        default = None
    )

    gas_equipment: GasEquipmentAbridged = Schema(
        default = None
    )

    infiltration : InfiltrationAbridged = Schema(
        default = None
    )

    ventilation : VentilationAbridged = Schema(
        default = None
    )

    setpoint: SetpointAbridged = Schema(
        default = None
    )

if __name__ == '__main__':

    print(ProgramTypeAbridged.schema_json(indent=2))
