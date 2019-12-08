"""Simulation Parameter Schema"""
from pydantic import BaseModel, Schema, validator
from typing import List
from enum import Enum
from ..datetime import Date


class ReportingFrequency(str, Enum):
    timestep = 'Timestep'
    hourly = 'Hourly'
    daily = 'Daily'
    monthly = 'Monthly'
    annual = 'Annual'


class SimulationOutput(BaseModel):
    """Lists the desired outputs from the simulation and the format in which to report them."""

    type: Enum('SimulationOutput', {'type': 'SimulationOutput'})

    reporting_frequency: ReportingFrequency = ReportingFrequency.hourly

    include_sqlite: bool = Schema(
        default=True
    )

    include_html: bool = Schema(
        default=False
    )

    outputs: List[str] = Schema(
        default=None
    )

    summary_reports: List[str] = Schema(
        default=None
    )


class SimulationControl(BaseModel):
    """Used to specify which types of calculations to run."""

    type: Enum('SimulationControl', {'type': 'SimulationControl'})

    do_zone_sizing: bool = Schema(
        default=True
    )

    do_system_sizing: bool = Schema(
        default=True
    )

    do_plant_sizing: bool = Schema(
        default=True
    )

    run_for_run_periods: bool = Schema(
        default=True
    )

    run_for_sizing_periods: bool = Schema(
        default=False
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

    type: Enum('ShadowCalculation', {'type': 'ShadowCalculation'})

    solar_distribution: SolarDistribution = SolarDistribution.full_interior_and_exterior_with_reflections

    calculation_frequency: int = Schema(
        30,
        ge=1
    )

    calculation_method: CalculationMethod = CalculationMethod.average_over_days_in_frequency

    maximum_figures: int = Schema(
        15000,
        ge=200,
        description='Number of allowable figures in shadow overlap calculations.'
    )


class SizingParameter(BaseModel):
    """Allows the user to specify global heating and cooling sizing ratios."""

    type: Enum('SizingParameter', {'type': 'SizingParameter'})

    heating_factor: float = Schema(
        1.25,
        gt=0,
        description='The global heating sizing ratio applied to all of the zone design heating loads and air flow rates.'
    )

    cooling_factor: float = Schema(
        1.15,
        gt=0,
        description='The global cooling sizing ratio applied to all of the zone design cooling loads and air flow rates.'
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

    type: Enum('DaylightSavingTime', {'type': 'DaylightSavingTime'})

    start_date: Date

    end_date: Date


class RunPeriod(BaseModel):
    """Used to describe the time period over which to run the simulation."""

    type: Enum('RunPeriod', {'type': 'RunPeriod'})

    start_date: Date

    end_date: Date

    start_day_of_week: DaysOfWeek = DaysOfWeek.sunday

    holidays: List[Date] = Schema(
        default=None
    )

    daylight_savings_time: DaylightSavingTime = Schema(
        default=None
    )


class SimulationParameter(BaseModel):
    """It is the complete set of EnergyPlus Simulation Settings."""

    type: Enum('SimulationParameter', {'type': 'SimulationParameter'})

    output: SimulationOutput = Schema(
        default=None
    )

    run_period: RunPeriod = Schema(
        default=None
    )

    timestep: int = Schema(
        default=6,
        ge=1
    )

    @validator('timestep')
    def check_values(cls, v):
        x = [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]
        if v not in x:
            raise ValueError('"{}" is not a valid timestep.'.format(v))
            
    simulation_control: SimulationControl = Schema(
        default=None
    )

    shadow_calculation: ShadowCalculation = Schema(
        default=None
    )

    sizing_parameter: SizingParameter = Schema(
        default=None
    )


if __name__ == '__main__':
    print(SimulationParameter.schema_json(indent=2))
