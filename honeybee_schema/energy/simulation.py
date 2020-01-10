"""Simulation Parameter Schema"""
from pydantic import BaseModel, Field, validator, constr
from typing import List
from enum import Enum

from .designday import DesignDay
from ..datetime import Date


class ReportingFrequency(str, Enum):
    timestep = 'Timestep'
    hourly = 'Hourly'
    daily = 'Daily'
    monthly = 'Monthly'
    annual = 'Annual'


class SimulationOutput(BaseModel):
    """Lists the outputs to report from the simulation and their format."""

    type: constr(regex='^SimulationOutput$') = 'SimulationOutput'

    reporting_frequency: ReportingFrequency = ReportingFrequency.hourly

    include_sqlite: bool = Field(
        default=True,
        description='Boolean to note whether a SQLite report should be generated '
            'from the simulation.'
    )

    include_html: bool = Field(
        default=False,
        description='Boolean to note whether an HTML report should be generated '
            'from the simulation.'
    )

    outputs: List[str] = Field(
        default=None,
        description='A list of EnergyPlus output names as strings, which are requested '
            'from the simulation.'
    )

    summary_reports: List[str] = Field(
        default=None,
        description='A list of EnergyPlus summary report names as strings.'
    )


class SimulationControl(BaseModel):
    """Used to specify which types of calculations to run."""

    type: constr(regex='^SimulationControl$') = 'SimulationControl'

    do_zone_sizing: bool = Field(
        default=True,
        description='Boolean for whether the zone sizing calculation should be run.'
    )

    do_system_sizing: bool = Field(
        default=True,
        description='Boolean for whether the system sizing calculation should be run.'
    )

    do_plant_sizing: bool = Field(
        default=True,
        description='Boolean for whether the plant sizing calculation should be run.'
    )

    run_for_run_periods: bool = Field(
        default=True,
        description='Boolean for whether the simulation should be run for the '
            'sizing periods.'
    )

    run_for_sizing_periods: bool = Field(
        default=False,
        description='Boolean for whether the simulation should be run for the '
            'run periods.'
    )


class SolarDistribution(str, Enum):
    minimal_shadowing = 'MinimalShadowing'
    full_exterior = 'FullExterior'
    full_interior_and_exterior = 'FullInteriorAndExterior'
    full_exterior_with_reflection = 'FullExteriorWithReflections'
    full_interior_and_exterior_with_reflections = 'FullInteriorAndExteriorWithReflections'


class CalculationMethod(str, Enum):
    average_over_days_in_frequency = 'AverageOverDaysInFrequency'
    timestep_frequency = 'TimestepFrequency'


class ShadowCalculation(BaseModel):
    """Used to describe settings for EnergyPlus shadow calculation."""

    type: constr(regex='^ShadowCalculation$') = 'ShadowCalculation'

    solar_distribution: SolarDistribution = \
        SolarDistribution.full_interior_and_exterior_with_reflections

    calculation_frequency: int = Field(
        30,
        ge=1,
        description='Integer for the number of days in each period for which a '
            'unique shadow calculation will be performed. This field is only used '
            'if the AverageOverDaysInFrequency calculation_method is used.'
    )

    calculation_method: CalculationMethod = \
        CalculationMethod.average_over_days_in_frequency

    maximum_figures: int = Field(
        15000,
        ge=200,
        description='Number of allowable figures in shadow overlap calculations.'
    )


class DaysOfWeek(str, Enum):
    sunday = 'Sunday'
    monday = 'Monday'
    tuesday = 'Tuesday'
    wednesday = 'Wednesday'
    thursday = 'Thursday'
    friday = 'Friday'
    saturday = 'Saturday'


class DaylightSavingTime(BaseModel):
    """Used to describe the daylight savings time for the simulation."""

    type: constr(regex='^DaylightSavingTime$') = 'DaylightSavingTime'

    start_date: Date

    end_date: Date


class RunPeriod(BaseModel):
    """Used to describe the time period over which to run the simulation."""

    type: constr(regex='^RunPeriod$') = 'RunPeriod'

    start_date: Date

    end_date: Date

    start_day_of_week: DaysOfWeek = DaysOfWeek.sunday

    holidays: List[Date] = Field(
        default=None
    )

    daylight_savings_time: DaylightSavingTime = Field(
        default=None
    )


class SizingParameter(BaseModel):
    """Used to specify heating and cooling sizing criteria and safety factors."""

    type: constr(regex='^SizingParameter$') = 'SizingParameter'

    design_days: List[DesignDay] = Field(
        default=None,
        description='A list of DesignDays that represent the criteria for which '
            'the HVAC systems will be sized.'
    )

    heating_factor: float = Field(
        1.25,
        gt=0,
        description='A number that will be multiplied by the peak heating load'
            ' for each zone in order to size the heating system.'
    )

    cooling_factor: float = Field(
        1.15,
        gt=0,
        description='A number that will be multiplied by the peak cooling load'
            ' for each zone in order to size the heating system.'
    )


class SimulationParameter(BaseModel):
    """The complete set of EnergyPlus Simulation Settings."""

    type: constr(regex='^SimulationParameter$') = 'SimulationParameter'

    output: SimulationOutput = Field(
        default=None,
        description='A SimulationOutput that lists the desired outputs from the '
            'simulation and the format in which to report them.'
    )

    run_period: RunPeriod = Field(
        default=None,
        description='A RunPeriod to describe the time period over which to '
            'run the simulation.'
    )

    timestep: int = Field(
        default=6,
        ge=1,
        le=60,
        description='An integer for the number of timesteps per hour at which the '
            'energy calculation will be run.'
    )

    @validator('timestep')
    def check_values(cls, v):
        valid_timesteps = (1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60)
        assert v in valid_timesteps, \
            '"{}" is not a valid timestep. Choose from {}'.format(v, valid_timesteps)
            
    simulation_control: SimulationControl = Field(
        default=None,
        description='A SimulationControl object that describes which types of '
            'calculations to run.'
    )

    shadow_calculation: ShadowCalculation = Field(
        default=None,
        description='A ShadowCalculation object describing settings for the '
            'EnergyPlus Shadow Calculation.'
    )

    sizing_parameter: SizingParameter = Field(
        default=None,
        description='A SizingParameter object with criteria for sizing the '
            'heating and cooling system.'
    )


if __name__ == '__main__':
    print(SimulationParameter.schema_json(indent=2))
