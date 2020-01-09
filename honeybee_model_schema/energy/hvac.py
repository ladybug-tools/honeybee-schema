"""Ideal Air Schema"""
from pydantic import BaseModel, Field, validator
from typing import Union
from enum import Enum

class EconomizerType(str, Enum):
    no_economizer = 'NoEconomizer'
    differential_dry_bulb = 'DifferentialDryBulb'
    differential_enthalpy = 'DifferentialEnthalpy'


class IdealAirSystem(BaseModel):
    """ Provides a model for an ideal HVAC system."""
    type: Enum('IdealAirSystem', {'type': 'IdealAirSystem'})

    heating_limit: Union[float, str] = Field(
        'autosize',
        ge=0
    )

    @validator('heating_limit')
    def check_string_heating_limit(cls, v):
        if not isinstance(v ,float) and v != 'autosize' and v != 'NoLimit':
            raise ValueError( 'This is not a valid entry for heating_limit')


    cooling_limit: Union[float, str] = Field(
        'autosize',
        ge=0
    )

    @validator('cooling_limit')
    def check_string_cooling_limit(cls, v):
        if not isinstance(v, float) and v != 'autosize' and v != 'NoLimit':
            raise ValueError( 'This is not a valid entry for cooling_limit')

    economizer_type: EconomizerType = EconomizerType.differential_dry_bulb

    demand_control_ventilation: bool = Field(
        False
    )

    sensible_heat_recovery: float = Field(
        0,
        ge=0,
        le=1
    )

    latent_heat_recovery: float = Field(
        0,
        ge=0,
        le=1
    )


if __name__ == '__main__':
    print(IdealAirSystem.schema_json(indent=2))
