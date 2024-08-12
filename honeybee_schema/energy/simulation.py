"""Simulation Parameter Schema"""
from pydantic import Field, validator, root_validator, constr, conlist
from typing import List
from enum import Enum

from .._base import NoExtraBaseModel
from ._base import DatedBaseModel
from .designday import DesignDay


class ReportingFrequency(str, Enum):
    timestep = 'Timestep'
    hourly = 'Hourly'
    daily = 'Daily'
    monthly = 'Monthly'
    annual = 'Annual'


class SimulationOutput(NoExtraBaseModel):
    """Lists the outputs to report from the simulation and their format."""

    type: constr(regex='^SimulationOutput$') = 'SimulationOutput'

    reporting_frequency: ReportingFrequency = ReportingFrequency.hourly

    outputs: List[str] = Field(
        default=None,
        description='A list of EnergyPlus output names as strings, which are requested '
        'from the simulation.'
    )

    summary_reports: List[str] = Field(
        default=None,
        description='A list of EnergyPlus summary report names as strings.'
    )

    unmet_setpoint_tolerance: float = Field(
        1.11,
        ge=0,
        le=10,
        description='A number in degrees Celsius for the difference that '
        'the zone conditions must be from the thermostat setpoint in order '
        'for the setpoint to be considered unmet. This will affect how unmet '
        'hours are reported in the output. ASHRAE 90.1 uses a tolerance of '
        '1.11C, which is equivalent to 1.8F.'
    )


class SimulationControl(NoExtraBaseModel):
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
    full_interior_and_exterior_with_reflections = \
        'FullInteriorAndExteriorWithReflections'


class CalculationMethod(str, Enum):
    polygon_clipping = 'PolygonClipping'
    pixel_counting = 'PixelCounting'


class CalculationUpdateMethod(str, Enum):
    periodic = 'Periodic'
    timestep = 'Timestep'


class ShadowCalculation(NoExtraBaseModel):
    """Used to describe settings for EnergyPlus shadow calculation."""

    type: constr(regex='^ShadowCalculation$') = 'ShadowCalculation'

    solar_distribution: SolarDistribution = \
        SolarDistribution.full_exterior_with_reflection

    calculation_method: CalculationMethod = Field(
        CalculationMethod.polygon_clipping,
        description='Text noting whether CPU-based polygon clipping method or'
        'GPU-based pixel counting method should be used. For low numbers of shading'
        'surfaces (less than ~200), PolygonClipping requires less runtime than'
        'PixelCounting. However, PixelCounting runtime scales significantly'
        'better at higher numbers of shading surfaces. PixelCounting also has'
        'no limitations related to zone concavity when used with any'
        '“FullInterior” solar distribution options.'
    )

    calculation_update_method: CalculationUpdateMethod = Field(
        CalculationUpdateMethod.periodic,
        description='Text describing how often the solar and shading calculations '
        'are updated with respect to the flow of time in the simulation.'
    )

    calculation_frequency: int = Field(
        30,
        ge=1,
        description='Integer for the number of days in each period for which a '
        'unique shadow calculation will be performed. This field is only used '
        'if the Periodic calculation_method is used.'
    )

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


class DaylightSavingTime(DatedBaseModel):
    """Used to describe the daylight savings time for the simulation."""

    type: constr(regex='^DaylightSavingTime$') = 'DaylightSavingTime'

    start_date: List[int] = Field(
        [3, 12],
        min_items=2,
        max_items=3,
        description='A list of two integers for [month, day], representing the date '
        'for the start of daylight savings time. Default: 12 Mar (daylight savings '
        'in the US in 2017).'
    )

    @validator('start_date')
    def check_start_date(cls, v):
        return cls.check_date(v)

    end_date: List[int] = Field(
        [11, 5],
        min_items=2,
        max_items=3,
        description='A list of two integers for [month, day], representing the date '
        'for the end of daylight savings time. Default: 5 Nov (daylight savings '
        'in the US in 2017).'
    )

    @validator('end_date')
    def check_end_date(cls, v):
        return cls.check_date(v)


class RunPeriod(DatedBaseModel):
    """Used to describe the time period over which to run the simulation."""

    type: constr(regex='^RunPeriod$') = 'RunPeriod'

    start_date: List[int] = Field(
        [1, 1],
        min_items=2,
        max_items=2,
        description='A list of two integers for [month, day], representing the date '
        'for the start of the run period. Must be before the end date.'
    )

    end_date: List[int] = Field(
        [12, 31],
        min_items=2,
        max_items=2,
        description='A list of two integers for [month, day], representing the date '
        'for the end of the run period. Must be after the start date.'
    )

    start_day_of_week: DaysOfWeek = Field(
        default=DaysOfWeek.sunday,
        description='Text for the day of the week on which the simulation starts.'
    )

    holidays: List[conlist(int, min_items=2, max_items=2)] = Field(
        default=None,
        description='A list of lists where each sub-list consists of two integers '
        'for [month, day], representing a date which is a holiday within the '
        'simulation. If None, no holidays are applied.'
    )

    daylight_saving_time: DaylightSavingTime = Field(
        default=None,
        description='A DaylightSavingTime to dictate the start and end dates '
        'of daylight saving time. If None, no daylight saving time is applied '
        'to the simulation.'
    )

    leap_year: bool = Field(
        default=False,
        description='Boolean noting whether the simulation will be run for a leap year.'
    )

    @root_validator
    def check_dates(cls, values):
        """Check that all of the input dates are valid."""
        start_date = values.get('start_date')
        end_date = values.get('end_date')
        holidays = values.get('holidays')
        leap_year = values.get('leap_year')
        cls.check_date(start_date, leap_year)
        cls.check_date(end_date, leap_year)
        if holidays is not None:
            for hol in holidays:
                cls.check_date(hol, leap_year)
        return values


class EfficiencyStandards(str, Enum):
    ashrae_2019 = 'ASHRAE_2019'
    ashrae_2016 = 'ASHRAE_2016'
    ashrae_2013 = 'ASHRAE_2013'
    ashrae_2010 = 'ASHRAE_2010'
    ashrae_2007 = 'ASHRAE_2007'
    ashrae_2004 = 'ASHRAE_2004'
    doe_ref_1980_2004 = 'DOE_Ref_1980_2004'
    doe_ref_pre_1980 = 'DOE_Ref_Pre_1980'


class ClimateZones(str, Enum):
    zone_0A = '0A'
    zone_1A = '1A'
    zone_2A = '2A'
    zone_3A = '3A'
    zone_4A = '4A'
    zone_5A = '5A'
    zone_6A = '6A'
    zone_0B = '0B'
    zone_1B = '1B'
    zone_2B = '2B'
    zone_3B = '3B'
    zone_4B = '4B'
    zone_5B = '5B'
    zone_6B = '6B'
    zone_3C = '3C'
    zone_4C = '4C'
    zone_5C = '5C'
    zone_7 = '7'
    zone_8 = '8'


class BuildingTypes(str, Enum):
    Residential = 'Residential'
    NonResidential = 'NonResidential'
    MidriseApartment = 'MidriseApartment'
    HighriseApartment = 'HighriseApartment'
    LargeOffice = 'LargeOffice'
    MediumOffice = 'MediumOffice'
    SmallOffice = 'SmallOffice'
    Retail = 'Retail'
    StripMall = 'StripMall'
    PrimarySchool = 'PrimarySchool'
    SecondarySchool = 'SecondarySchool'
    SmallHotel = 'SmallHotel'
    LargeHotel = 'LargeHotel'
    Hospital = 'Hospital'
    Outpatient = 'Outpatient'
    Warehouse = 'Warehouse'
    SuperMarket = 'SuperMarket'
    FullServiceRestaurant = 'FullServiceRestaurant'
    QuickServiceRestaurant = 'QuickServiceRestaurant'
    Laboratory = 'Laboratory'
    Courthouse = 'Courthouse'


class SizingParameter(NoExtraBaseModel):
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

    efficiency_standard: EfficiencyStandards = Field(
        default=None,
        description='Text to specify the efficiency standard, which will '
        'automatically set the efficiencies of all HVAC equipment when provided. '
        'Note that providing a standard here will cause the OpenStudio translation '
        'process to perform an additional sizing calculation with EnergyPlus, '
        'which is needed since the default efficiencies of equipment vary depending '
        'on their size. THIS WILL SIGNIFICANTLY INCREASE TRANSLATION TIME TO '
        'OPENSTUDIO. However, it is often worthwhile when the goal is to match the '
        'HVAC specification with a particular standard.'
    )

    climate_zone: ClimateZones = Field(
        default=None,
        description='Text indicating the ASHRAE climate zone to be used with the '
        'efficiency_standard. When unspecified, the climate zone will be inferred from '
        'the design days on this sizing parameter object.'
    )

    building_type: str = Field(
        default=None,
        description='Text for the building type to be used in the efficiency_standard. '
        'If the type is not recognized or is None, it will be assumed that the building '
        'is a generic NonResidential. The following have specified systems per the '
        'standard:  Residential, NonResidential, MidriseApartment, HighriseApartment, '
        'LargeOffice, MediumOffice, SmallOffice, Retail, StripMall, '
        'PrimarySchool, SecondarySchool, SmallHotel, LargeHotel, Hospital, Outpatient, '
        'Warehouse, SuperMarket, FullServiceRestaurant, QuickServiceRestaurant, '
        'Laboratory, Courthouse.'
    )

    bypass_efficiency_sizing: bool = Field(
        default=False,
        description='A boolean to indicate whether the efficiency standard should '
        'trigger an sizing run that sets the efficiencies of all HVAC equipment in '
        'the Model (False) or the standard should only be written into the OSM and '
        'the sizing run should be bypassed (True). Bypassing the sizing run is useful '
        'when you only want to check that the overall HVAC system architecture is '
        'correct and you do not want to wait the extra time that it takes to run the '
        'sizing calculation.'
    )


class TerrianTypes(str, Enum):
    ocean = 'Ocean'
    country = 'Country'
    suburbs = 'Suburbs'
    urban = 'Urban'
    city = 'City'


class SimulationParameter(NoExtraBaseModel):
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
    def check_timestep(cls, v):
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

    north_angle: float = Field(
        default=0,
        ge=-360,
        le=360,
        description='A number between -360 and 360 for the north direction in degrees.'
        'This is the counterclockwise difference between the North and the '
        'positive Y-axis. 90 is West and 270 is East. Note that this '
        'is different than the convention used in EnergyPlus, which uses '
        'clockwise difference instead of counterclockwise difference.'
    )

    terrain_type: TerrianTypes = Field(
        default=TerrianTypes.city,
        description='Text for the terrain in which the model sits. This is used '
        'to determine the wind profile over the height of the rooms.'
    )
