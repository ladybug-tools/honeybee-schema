"""Ideal Air Schema"""
from pydantic import Field, root_validator, constr
from typing import Union
from enum import Enum

from .._base import IDdEnergyBaseModel
from ...altnumber import NoLimit, Autosize


class EconomizerType(str, Enum):
    no_economizer = 'NoEconomizer'
    differential_dry_bulb = 'DifferentialDryBulb'
    differential_enthalpy = 'DifferentialEnthalpy'


class IdealAirSystemAbridged(IDdEnergyBaseModel):
    """ Provides a model for an ideal HVAC system."""

    type: constr(regex='^IdealAirSystemAbridged$') = 'IdealAirSystemAbridged'

    economizer_type: EconomizerType = Field(
        EconomizerType.differential_dry_bulb,
        description='Text to indicate the type of air-side economizer used on the '
        'ideal air system. Economizers will mix in a greater amount of outdoor '
        'air to cool the zone (rather than running the cooling system) when '
        'the zone needs cooling and the outdoor air is cooler than the zone.'
    )

    demand_controlled_ventilation: bool = Field(
        False,
        description='Boolean to note whether demand controlled ventilation should '
        'be used on the system, which will vary the amount of ventilation air '
        'according to the occupancy schedule of the zone.'
    )

    sensible_heat_recovery: float = Field(
        0,
        ge=0,
        le=1,
        description='A number between 0 and 1 for the effectiveness of sensible '
        'heat recovery within the system.'
    )

    latent_heat_recovery: float = Field(
        0,
        ge=0,
        le=1,
        description='A number between 0 and 1 for the effectiveness of latent '
        'heat recovery within the system.'
    )

    heating_air_temperature: float = Field(
        50,
        gt=0,
        lt=100,
        description='A number for the maximum heating supply air temperature [C].'
    )

    cooling_air_temperature: float = Field(
        13,
        gt=-100,
        lt=50,
        description='A number for the minimum cooling supply air temperature [C].'
    )

    heating_limit: Union[Autosize, NoLimit, float] = Field(
        Autosize(),
        ge=0,
        description='A number for the maximum heating capacity in Watts. This '
        'can also be an Autosize object to indicate that the capacity should '
        'be determined during the EnergyPlus sizing calculation. This can also '
        'be a NoLimit object to indicate no upper limit to the heating capacity.'
    )

    cooling_limit: Union[Autosize, NoLimit, float] = Field(
        Autosize(),
        ge=0,
        description='A number for the maximum cooling capacity in Watts. This '
        'can also be an Autosize object to indicate that the capacity should '
        'be determined during the EnergyPlus sizing calculation. This can also '
        'be a NoLimit object to indicate no upper limit to the cooling capacity.'
    )

    heating_availability: str = Field(
        None,
        min_length=1,
        max_length=100,
        description='An optional identifier of a schedule to set the availability of '
        'heating over the course of the simulation.'
    )

    cooling_availability: str = Field(
        None,
        min_length=1,
        max_length=100,
        description='An optional identifier of a schedule to set the availability of '
        'cooling over the course of the simulation.'
    )

    @root_validator
    def check_heating_temp_gt_cooling_temp(cls, values):
        "Ensure that the heating_air_temperature > cooling_air_temperature."
        heat_temp = values.get('heating_air_temperature')
        cool_temp = values.get('cooling_air_temperature')
        assert heat_temp > cool_temp, 'IdealAirSystem heating_air_temperature must be ' \
            'greater than cooling_air_temperature.'
        return values
