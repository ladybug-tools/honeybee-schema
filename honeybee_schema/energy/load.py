"""Load Schemas"""
from pydantic import Field, model_validator
from typing import Union, Literal, Annotated
from enum import Enum

from ._base import IDdEnergyBaseModel
from .schedule import ScheduleRuleset, ScheduleFixedInterval
from ..altnumber import Autocalculate


class PeopleAbridged(IDdEnergyBaseModel):

    type: Literal['PeopleAbridged'] = 'PeopleAbridged'

    people_per_area: float = Field(
        ...,
        ge=0,
        description='People per floor area expressed as [people/m2]'
    )

    occupancy_schedule: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of a schedule for the occupancy over the course of the '
        'year. The type of this schedule should be Fractional and the fractional '
        'values will get multiplied by the people_per_area to yield a complete '
        'occupancy profile. If None, an Always On schedule will be used.'
    )

    activity_schedule: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of a schedule for the activity of the occupants over '
        'the course of the year. The type of this schedule should be ActivityLevel '
        'and the values of the schedule equal to the number of Watts given off by an '
        'individual person in the room. If None, a default constant schedule with '
        '120 Watts per person will be used, which is typical of awake, adult humans '
        'who are seated.'
    )

    radiant_fraction: float = Field(
        0.3,
        ge=0,
        le=1,
        description='The radiant fraction of sensible heat released by people. '
        '(Default: 0.3).'
    )

    latent_fraction: Union[Autocalculate, Annotated[float, Field(ge=0, le=1)]] = Field(
        Autocalculate(),
        description='Number for the latent fraction of heat gain due to people or '
        'an Autocalculate object.'
    )

    @model_validator(mode='after')
    def check_sum_fractions(self) -> 'PeopleAbridged':
        "Ensure sum is less than 1."
        if self.latent_fraction is not None and isinstance(self.latent_fraction, float):
            assert self.radiant_fraction + self.latent_fraction <= 1, \
                'Sum of radiant and latent fractions cannot be greater than 1.'
        return self


class People(PeopleAbridged):

    type: Literal['People'] = 'People'

    occupancy_schedule: Union[ScheduleRuleset, ScheduleFixedInterval, None] = Field(
        default=None,
        description='A schedule for the occupancy over the course of the '
        'year. The type of this schedule should be Fractional and the fractional '
        'values will get multiplied by the people_per_area to yield a complete '
        'occupancy profile. If None, an Always On schedule will be used.'
    )

    activity_schedule: Union[ScheduleRuleset, ScheduleFixedInterval, None] = Field(
        default=None,
        description='A schedule for the activity of the occupants over the '
        'course of the year. The type of this schedule should be ActivityLevel '
        'and the values of the schedule equal to the number of Watts given off by an '
        'individual person in the room. If None, a default constant schedule with '
        '120 Watts per person will be used, which is typical of awake, adult humans '
        'who are seated.'
    )


class LightingAbridged(IDdEnergyBaseModel):

    type: Literal['LightingAbridged'] = 'LightingAbridged'

    watts_per_area: float = Field(
        ...,
        ge=0,
        description='Lighting per floor area as [W/m2].'
    )

    schedule: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of the schedule for the use of lights over the course '
        'of the year. The type of this schedule should be Fractional and the '
        'fractional values will get multiplied by the watts_per_area to yield a '
        'complete lighting profile. If None, an Always On schedule will be used.'
    )

    visible_fraction: float = Field(
        0.25,
        ge=0,
        le=1,
        description='The fraction of heat from lights that goes into the zone as '
        'visible (short-wave) radiation. (Default: 0.25).'
    )

    radiant_fraction: float = Field(
        0.32,
        ge=0,
        le=1,
        description='The fraction of heat from lights that is long-wave radiation. '
        '(Default: 0.32).'
    )

    return_air_fraction: float = Field(
        0.0,
        ge=0,
        le=1,
        description='The fraction of the heat from lights that goes into the zone '
        'return air. (Default: 0).'
    )

    baseline_watts_per_area: float = Field(
        11.84029,
        ge=0,
        description='The baseline lighting power density in [W/m2] of floor area. '
        'This baseline is useful to track how much better the installed lights are '
        'in comparison to a standard like ASHRAE 90.1. If set to None, it will '
        'default to 11.84029 W/m2, which is that ASHRAE 90.1-2004 baseline for '
        'an office.'
    )

    @model_validator(mode='after')
    def check_sum_fractions(self) -> 'LightingAbridged':
        "Ensure sum is less than 1."
        assert sum((self.return_air_fraction, self.visible_fraction,
                    self.radiant_fraction)) <= 1, \
            'Sum of visible, radiant, and return air fractions cannot be greater than 1.'
        return self


class Lighting(LightingAbridged):

    type: Literal['Lighting'] = 'Lighting'

    schedule: Union[ScheduleRuleset, ScheduleFixedInterval, None] = Field(
        default=None,
        description='The schedule for the use of lights over the course of '
        'the year. The type of this schedule should be Fractional and the '
        'fractional values will get multiplied by the watts_per_area to yield a '
        'complete lighting profile. If None, an Always On schedule will be used.'
    )


class _EquipmentBase(IDdEnergyBaseModel):

    watts_per_area: float = Field(
        ...,
        ge=0,
        description='Equipment level per floor area as [W/m2].'
    )

    schedule: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of the schedule for the use of equipment over the '
        'course of the year. The type of this schedule should be Fractional and the '
        'fractional values will get multiplied by the watts_per_area to yield '
        'a complete equipment profile. If None, an Always On schedule will be used.'
    )

    radiant_fraction: float = Field(
        0,
        ge=0,
        le=1,
        description='Number for the amount of long-wave radiation heat given off'
        ' by equipment. Default value is 0.'
    )

    latent_fraction: float = Field(
        0,
        ge=0,
        le=1,
        description='Number for the amount of latent heat given off by '
        'equipment. Default value is 0.'

    )

    lost_fraction: float = Field(
        0,
        ge=0,
        le=1,
        description='Number for the amount of “lost” heat being given off by '
        'equipment. The default value is 0.'
    )

    @model_validator(mode='after')
    def check_sum_fractions(self) -> '_EquipmentBase':
        "Ensure sum is less than 1."
        assert sum((self.radiant_fraction, self.latent_fraction, self.lost_fraction)) <= 1, \
            'Sum of radiant, latent, and lost fractions cannot be greater than 1.'
        return self


class ElectricEquipmentAbridged(_EquipmentBase):

    type: Literal['ElectricEquipmentAbridged'] = 'ElectricEquipmentAbridged'


class ElectricEquipment(ElectricEquipmentAbridged):

    type: Literal['ElectricEquipment'] = 'ElectricEquipment'

    schedule: Union[ScheduleRuleset, ScheduleFixedInterval, None] = Field(
        default=None,
        description='The schedule for the use of equipment over the course '
        'of the year. The type of this schedule should be Fractional and the '
        'fractional values will get multiplied by the watts_per_area to yield '
        'a complete equipment profile. If None, an Always On schedule will be used.'
    )


class GasEquipmentAbridged(_EquipmentBase):

    type: Literal['GasEquipmentAbridged'] = 'GasEquipmentAbridged'


class GasEquipment(GasEquipmentAbridged):

    type: Literal['GasEquipment'] = 'GasEquipment'

    schedule: Union[ScheduleRuleset, ScheduleFixedInterval, None] = Field(
        default=None,
        description='The schedule for the use of equipment over the course '
        'of the year. The type of this schedule should be Fractional and the '
        'fractional values will get multiplied by the watts_per_area to yield '
        'a complete equipment profile. If None, an Always On schedule will be used.'
    )


class ServiceHotWaterAbridged(IDdEnergyBaseModel):

    type: Literal['ServiceHotWaterAbridged'] = 'ServiceHotWaterAbridged'

    flow_per_area: float = Field(
        ...,
        ge=0,
        description='Number for the total volume flow rate of water per unit area '
        'of floor [L/h-m2].'
    )

    schedule: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of the schedule for the hot water use over the course '
        'of the year. The type of this schedule should be Fractional and the '
        'fractional values will get multiplied by the flow_per_area to yield a '
        'complete water usage profile. If None, an Always On schedule will be used.'
    )

    target_temperature: float = Field(
        60,
        gt=0,
        description='Number for the target temperature of water out of the tap (C). '
        'This the temperature after hot water has been mixed with cold water '
        'from the water mains. The default is 60C, which essentially assumes that the '
        'flow_per_area on this object is only for water straight out of the '
        'water heater.'
    )

    sensible_fraction: float = Field(
        0.2,
        ge=0,
        le=1,
        description='A number between 0 and 1 for the fraction of the total hot water '
        'load given off as sensible heat in the zone.'
    )

    latent_fraction: float = Field(
        0.05,
        ge=0,
        le=1,
        description='A number between 0 and 1 for the fraction of the total hot '
        'water load that is latent.'
    )

    @model_validator(mode='after')
    def check_sum_fractions(self) -> 'ServiceHotWaterAbridged':
        "Ensure sum is less than 1."
        assert sum((self.sensible_fraction, self.latent_fraction)) <= 1, \
            'Sum of sensible and latent fractions cannot be greater than 1.'
        return self


class ServiceHotWater(ServiceHotWaterAbridged):

    type: Literal['ServiceHotWater'] = 'ServiceHotWater'

    schedule: Union[ScheduleRuleset, ScheduleFixedInterval, None] = Field(
        default=None,
        description='The schedule for the use of hot water over the course of '
        'the year. The type of this schedule should be Fractional and the '
        'fractional values will get multiplied by the flow_per_area to yield a '
        'complete water usage profile. If None, an Always On schedule will be used.'
    )


class InfiltrationAbridged(IDdEnergyBaseModel):

    type: Literal['InfiltrationAbridged'] = 'InfiltrationAbridged'

    flow_per_exterior_area: float = Field(
        ...,
        ge=0,
        description='Number for the infiltration per exterior surface area in m3/s-m2.'
    )

    schedule: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of the schedule for the infiltration over the course of '
        'the year. The type of this schedule should be Fractional and the '
        'fractional values will get multiplied by the flow_per_exterior_area '
        'to yield a complete infiltration profile. If None, an Always On schedule '
        'will be used.'
    )

    constant_coefficient: float = Field(
        1,
        ge=0
    )

    temperature_coefficient: float = Field(
        0,
        ge=0
    )

    velocity_coefficient: float = Field(
        0,
        ge=0
    )


class Infiltration(InfiltrationAbridged):

    type: Literal['Infiltration'] = 'Infiltration'

    schedule: Union[ScheduleRuleset, ScheduleFixedInterval, None] = Field(
        default=None,
        description='The schedule for the infiltration over the course of '
        'the year. The type of this schedule should be Fractional and the '
        'fractional values will get multiplied by the flow_per_exterior_area '
        'to yield a complete infiltration profile. If None, an Always On schedule '
        'will be used.'
    )


class VentilationMethod(str, Enum):
    sum = 'Sum'
    max = 'Max'


class VentilationAbridged(IDdEnergyBaseModel):

    type: Literal['VentilationAbridged'] = 'VentilationAbridged'

    flow_per_person: float = Field(
        0,
        ge=0,
        description='Intensity of ventilation in[] m3/s per person]. Note that '
        'setting this value does not mean that ventilation is varied based on '
        'real-time occupancy but rather that the design level of ventilation '
        'is determined using this value and the People object of the Room.'
    )

    flow_per_area: float = Field(
        0,
        ge=0,
        description='Intensity of ventilation in [m3/s per m2 of floor area].'
    )

    air_changes_per_hour: float = Field(
        0,
        ge=0,
        description='Intensity of ventilation in air changes per hour (ACH) for '
        'the entire Room.'
    )

    flow_per_zone: float = Field(
        0,
        ge=0,
        description='Intensity of ventilation in m3/s for the entire Room.'
    )

    schedule: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of the schedule for the ventilation over the course of '
        'the year. The type of this schedule should be Fractional and the '
        'fractional values will get multiplied by the total design flow rate '
        '(determined from the sum of the other 4 fields) to yield a complete '
        'ventilation profile.'
    )

    method: VentilationMethod = Field(
        VentilationMethod.sum,
        description='Text to set how the ventilation criteria are reconciled '
        'against one another.'
    )


class Ventilation(VentilationAbridged):

    type: Literal['Ventilation'] = 'Ventilation'

    schedule: Union[ScheduleRuleset, ScheduleFixedInterval, None] = Field(
        default=None,
        description='Schedule for the ventilation over the course of '
        'the year. The type of this schedule should be Fractional and the '
        'fractional values will get multiplied by the total design flow rate '
        '(determined from the sum of the other 4 fields) to yield a complete '
        'ventilation profile.'
    )


class SetpointAbridged(IDdEnergyBaseModel):
    """Used to specify information about the setpoint schedule."""

    type: Literal['SetpointAbridged'] = 'SetpointAbridged'

    cooling_schedule: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='Identifier of the schedule for the cooling setpoint. The values in '
        'this schedule should be temperature in [C].'
    )

    heating_schedule: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='Identifier of the schedule for the heating setpoint. The values in '
        'this schedule should be temperature in [C].'
    )

    humidifying_schedule: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of the schedule for the humidification setpoint. '
        'The values in this schedule should be in [%].'
    )

    dehumidifying_schedule: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of the schedule for the dehumidification setpoint. '
        'The values in this schedule should be in [%].'
    )

    setpoint_cutout_difference: float = Field(
        0,
        ge=0,
        description='An optional positive number for the temperature '
        'difference between the cutout temperature and the setpoint temperature. '
        'Specifying a non-zero number here is useful for modeling the throttling '
        'range associated with a given setup of setpoint controls and HVAC equipment. '
        'Throttling ranges describe the range where a zone is slightly over-cooled '
        'or over-heated beyond the thermostat setpoint. They are used to avoid '
        'situations where HVAC systems turn on only to turn off a few minutes later, '
        'thereby wearing out the parts of mechanical systems faster. They can '
        'have a minor impact on energy consumption and can often have significant '
        'impacts on occupant thermal comfort, though using the default value '
        'of zero will often yield results that are close enough when trying '
        'to estimate the annual heating/cooling energy use. Specifying a value '
        'of zero effectively assumes that the system will turn on whenever '
        'conditions are outside the setpoint range and will cut out as soon '
        'as the setpoint is reached.'
    )

    @model_validator(mode='after')
    def check_both_humid_sch(self) -> 'SetpointAbridged':
        "Ensure that the other humidity schedule is included when one is."
        if self.humidifying_schedule is not None:
            assert self.dehumidifying_schedule is not None, 'When humidifying_schedule is specified, ' \
                'dehumidifying_schedule must also be specified.'
        if self.dehumidifying_schedule is not None:
            assert self.humidifying_schedule is not None, 'When dehumidifying_schedule is specified, ' \
                'humidifying_schedule must also be specified.'
        return self


class Setpoint(SetpointAbridged):
    """Used to specify information about the setpoint schedule."""

    type: Literal['Setpoint'] = 'Setpoint'

    cooling_schedule: Union[ScheduleRuleset, ScheduleFixedInterval] = Field(
        ...,
        description='Schedule for the cooling setpoint. The values in '
        'this schedule should be temperature in [C].'
    )

    heating_schedule: Union[ScheduleRuleset, ScheduleFixedInterval] = Field(
        ...,
        description='Schedule for the heating setpoint. The values in '
        'this schedule should be temperature in [C].'
    )

    humidifying_schedule: Union[ScheduleRuleset, ScheduleFixedInterval, None] = Field(
        default=None,
        description='Schedule for the humidification setpoint. The values '
        'in this schedule should be in [%].'
    )

    dehumidifying_schedule: Union[ScheduleRuleset, ScheduleFixedInterval, None] = Field(
        default=None,
        description='Schedule for the dehumidification setpoint. The values '
        'in this schedule should be in [%].'
    )


class FuelTypes (str, Enum):
    """Designates the acceptable fuel types for process loads."""
    electricity = 'Electricity'
    natural_gas = 'NaturalGas'
    propane = 'Propane'
    fuel_oil_no_1 = 'FuelOilNo1'
    fuel_oil_no_2 = 'FuelOilNo2'
    diesel = 'Diesel'
    gasoline = 'Gasoline'
    coal = 'Coal'
    steam = 'Steam'
    district_heating = 'DistrictHeating'
    district_cooling = 'DistrictCooling'
    other_fuel_1 = 'OtherFuel1'
    other_fuel_2 = 'OtherFuel2'
    none = 'None'


class ProcessAbridged(IDdEnergyBaseModel):

    type: Literal['ProcessAbridged'] = 'ProcessAbridged'

    watts: float = Field(
        ...,
        ge=0,
        description='A number for the process load power in Watts.'
    )

    schedule: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of the schedule for the use of the process over the '
        'course of the year. The type of this schedule should be Fractional and the '
        'fractional values will get multiplied by the watts to yield a complete '
        'equipment profile. If None, an Always On schedule will be used.'
    )

    fuel_type: FuelTypes = Field(
        FuelTypes.electricity,
        description='Text to denote the type of fuel consumed by the process. '
        'Using the "None" type indicates that no end uses will be associated '
        'with the process, only the zone gains.'
    )

    end_use_category: str = Field(
        'Process',
        min_length=1,
        max_length=100,
        description='Text to indicate the end-use subcategory, which will identify '
        'the process load in the end use output. For example, “Cooking”, '
        '“Clothes Drying”, etc. A new meter for reporting is created for each '
        'unique subcategory.'
    )

    radiant_fraction: float = Field(
        0,
        ge=0,
        le=1,
        description='Number for the amount of long-wave radiation heat given off'
        ' by the process load. Default value is 0.'
    )

    latent_fraction: float = Field(
        0,
        ge=0,
        le=1,
        description='Number for the amount of latent heat given off by the process '
        'load. Default value is 0.'

    )

    lost_fraction: float = Field(
        0,
        ge=0,
        le=1,
        description='Number for the amount of “lost” heat being given off by '
        'the process load. The default value is 0.'
    )

    @model_validator(mode='after')
    def check_sum_fractions(self) -> 'ProcessAbridged':
        "Ensure sum is less than 1."
        assert sum((self.radiant_fraction, self.latent_fraction, self.lost_fraction)) <= 1, \
            'Sum of radiant, latent, and lost fractions cannot be greater than 1.'
        return self
