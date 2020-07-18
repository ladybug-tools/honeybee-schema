"""Programtype Schema"""
from pydantic import Field, constr

from .._base import NoExtraBaseModel
from enum import Enum


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
        'Default: 0.5.'
    )

    fraction_height_operable: float = Field(
        1.0,
        ge=0,
        le=1,
        description='A number for the fraction of the distance from the bottom of the '
        'window to the top that is operable. Default: 1.0.'
    )

    discharge_coefficient: float = Field(
        0.45,
        ge=0,
        le=1,
        description='A number that will be multipled by the area of the window in the '
        'stack (buoyancy-driven) part of the equation to account for additional '
        'friction from window geometry, insect screens, etc. Typical values include '
        '0.45, for unobstructed windows WITH insect screens and 0.65 for unobstructed '
        'windows WITHOUT insect screens. This value should be lowered if windows are '
        'of an awning or casement type and are not allowed to fully open.'
    )

    wind_cross_vent: bool = Field(
        False,
        description='Boolean to indicate if there is an opening of roughly equal area '
        'on the opposite side of the Room such that wind-driven cross ventilation will '
        'be induced. If False, the assumption is that the operable area is primarily on '
        'one side of the Room and there is no wind-driven ventilation. Default: False.'
    )

    air_mass_flow_coefficient_closed: float = Field(
        default=None,
        gt=0,
        description='A number in kg/s-m used to calculate the mass flow rate '
        '(air_mass_flow_coefficient * dP^air_mass_flow_exponent) when the opening is '
        'closed, defined at 1 Pa per meter of crack length. This property is only '
        'required if running an AirflowNetwork simulation.'
    )

    air_mass_flow_exponent_closed: float = Field(
        default=0.65,
        ge=0.5,
        le=1,
        description='A dimensionlesss number used to calculate the mass flow rate '
        '(air_mass_flow_coefficient * dP^air_mass_flow_exponent) when the opening is '
        'closed. This property is only required if running an AirflowNetwork simulation.'
        'Default: 0.65.'
    )

    minimum_density_difference_two_way_flow: float = Field(
        default=None,
        gt=0,
        description='Number indicating the minimum density difference above which '
        'two-way flow may occur due to stack effect.'
    )


class AFNCrack(NoExtraBaseModel):
    """Properties for airflow through a crack."""

    type: constr(regex='^AFNCrack$') = 'AFNCrack'

    air_mass_flow_coefficient_reference: float = Field(
        ...,
        gt=0,
        description='The air mass flow coefficient in kg/s at the conditions defined in '
        'the AFNReferenceCrack condition, defined at a 1 Pa difference across this '
        'crack.'
    )

    air_mass_flow_exponent: float = Field(
        default=0.65,
        ge=0.5,
        le=1,
        description='The air mass flow exponent for the surface crack. Default: 0.65.'
    )

    crack_factor: float = Field(
        default=1,
        gt=0,
        le=1,
        description='A number indicating multiplier for air mass flow through a crack.'
        'Default: 1.'
    )


class AFNControlType(str, Enum):
    multizone_with_distribution = 'MultiZoneWithDistribution'
    multizone_without_distribution = 'MultiZoneWithoutDistribution'
    multizone_with_distribution_only_during_fan_operation = \
        'MultiZoneWithDistributionOnlyDuringFanOperation'


class AFNBuildingType(str, Enum):
    lowrise = 'LowRise'
    highrise = 'HighRise'


class AFNSimulationControl(NoExtraBaseModel):
    """The global parameters used in the Airflow Network simulation."""

    type: constr(regex='^AFNSimulationControl$') = 'AFNSimulationControl'

    afn_control_type: AFNControlType = Field(
        default=AFNControlType.multizone_without_distribution,
        description='Text indicating type of control for an Airflow Network simulation. '
        'Choices are: MultiZoneWithDistribution, MultiZoneWithoutDistribution, '
        'or MultiZoneWithDistributionOnlyDuringFanOperation.'
    )

    building_type: AFNBuildingType = Field(
        default=AFNBuildingType.lowrise,
        description='Text indicating relationship between building footprint and '
        'height used to calculate the wind pressure coefficients for exterior surfaces.'
        'Choices are: LowRise and HighRise. LowRise corresponds to rectangular building '
        'whose height is less then three times the width and length of the footprint. '
        'HighRise corresponds to rectangular building whose height is more than three '
        'times the width and length of the footprint. Default: LowRise.'
    )

    long_axis_angle: float = Field(
        default=0,
        ge=0,
        le=180,
        description='The clockwise rotation in degrees from true North of the long axis '
        'of the building. Default: 0.'
    )

    aspect_ratio: float = Field(
        default=1,
        gt=0,
        le=1,
        description='Aspect ratio of a rectangular footprint, defined as the ratio of '
        'length of the short axis divided by the length of the long axis. Default: 1.'
    )


class AFNReferenceCrack(NoExtraBaseModel):
    """Measurement conditions for air mass flow coefficients used by surface cracks."""

    type: constr(regex='^AFNReferenceCrack$') = 'AFNReferenceCrack'

    reference_temperature: float = Field(
        default=20,
        description='Reference temperature measurement in Celsius under which the '
        'surface crack data were obtained. Default: 20.'
    )

    reference_barometric_pressure: float = Field(
        default=101320,
        ge=31000,
        le=120000,
        description='Reference barometric pressure measurement in Pascals under which '
        'the surface crack data were obtained. Default 101320.'
    )

    reference_humidty_ratio: float = Field(
        default=0,
        ge=0,
        description='Reference humidity ratio measurement in kgWater/kgDryAir under '
        'which the surface crack data were obtained. Default: 0.'
    )


if __name__ == '__main__':
    print(VentilationControlAbridged.schema_json(indent=2))
    print(VentilationOpening.schema_json(indent=2))
    print(AFNSimulationControl.schema_json(indent=2))
    print(AFNReferenceCrack.schema_json(indent=2))
    print(AFNCrack.schema_json(indent=2))
