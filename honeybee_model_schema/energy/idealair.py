"""Ideal Air Schema"""
from pydantic import BaseModel, Schema, validator
from typing import Union
from enum import Enum

class EconomizerType(str, Enum):
    no_economizer = 'NoEconomizer'
    differential_dry_bulb = 'DifferentialDryBulb'
    differential_enthalpy = 'DifferentialEnthalpy'

class IdealAirLimitConfig(str, Enum):
    autosize = 'AutoSize'
    no_limit = 'NoLimit'
    fixed_value = 'FixedValue'

class IdealAirLimit(BaseModel):

    config: IdealAirLimitConfig = IdealAirLimitConfig.autosize

    value: float = Schema(
        default=None,
        ge=0
    )

    @validator('value')
    def check_config(cls, v, values, **kwargs):
        if 'value' in values and values['config'] == "FixedValue":
            raise ValueError('ideal air limit config should be "FixedValue" if value is not null')
        return v

class IdealAirSystem(BaseModel):
    """ Provides a model for an ideal HVAC system."""
    type: Enum('IdealAirSystem', {'type': 'IdealAirSystem'})

    heating_limit: IdealAirLimit = Schema(
        None
    )

    cooling_limit: IdealAirLimit = Schema(
        None
    )

    economizer_type: EconomizerType = EconomizerType.differential_dry_bulb

    demand_control_ventilation: bool = Schema(
        False
    )

    sensible_heat_recovery: float = Schema(
        0,
        ge=0,
        le=1
    )

    latent_heat_recovery: float = Schema(
        0,
        ge=0,
        le=1
    )
    