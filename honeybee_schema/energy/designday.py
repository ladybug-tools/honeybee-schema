"""Design Day Schema"""
from pydantic import Field, constr, validator
from typing import Union, List
from enum import Enum
import datetime

from .._base import NoExtraBaseModel


class DryBulbCondition(NoExtraBaseModel):
    """Used to specify dry bulb conditions on a design day."""

    type: constr(regex='^DryBulbCondition$') = 'DryBulbCondition'

    dry_bulb_max: float = Field(
        ...,
        ge=-90,
        le=70,
        description='The maximum dry bulb temperature on the design day [C].'
    )

    dry_bulb_range: float = Field(
        ...,
        ge=0,
        description='The difference between min and max temperatures on the '
        'design day [C].'
    )


class HumidityTypes(str, Enum):
    wetbulb = 'Wetbulb'
    dewpoint = 'Dewpoint'
    humidity_ratio = 'HumidityRatio'
    enthalpy = 'Enthalpy'


class HumidityCondition(NoExtraBaseModel):
    """Used to specify humidity conditions on a design day."""

    type: constr(regex='^HumidityCondition$') = 'HumidityCondition'

    humidity_type: HumidityTypes

    humidity_value: float = Field(
        ...,
        description='The value correcponding to the humidity_type.'
    )

    barometric_pressure: float = Field(
        101325,
        ge=31000,
        le=120000,
        description='Barometric air pressure on the design day [Pa].'
    )

    rain: bool = Field(
        default=False,
        description='Boolean to indicate rain on the design day.'
    )

    snow_on_ground: bool = Field(
        default=False,
        description='Boolean to indicate snow on the ground during the design day.'
    )


class WindCondition(NoExtraBaseModel):
    """Used to specify wind conditions on a design day."""

    type: constr(regex='^WindCondition$') = 'WindCondition'

    wind_speed: float = Field(
        ...,
        ge=0,
        le=40,
        description='Wind speed on the design day [m/s].'
    )

    wind_direction: float = Field(
        0,
        ge=0,
        le=360,
        description='Wind direction on the design day [degrees].'
    )


class _SkyCondition(NoExtraBaseModel):
    """Used to specify sky conditions on a design day."""

    date: List[int] = Field(
        ...,
        min_items=2,
        max_items=3,
        description='A list of two integers for [month, day], representing the date '
        'for the day of the year on which the design day occurs. '
        'A third integer may be added to denote whether the date should be '
        're-serialized for a leap year (it should be a 1 in this case).'
    )

    @validator('date')
    def check_date(cls, v):
        "Ensure valid date."
        if len(v) == 3 and v[2]:
            try:
                datetime.date(2016, v[0], v[1])
            except ValueError:
                raise ValueError('{}/{} is not a valid date.'.format(v[0], v[1]))
        else:
            try:
                datetime.date(2017, v[0], v[1])
            except ValueError:
                raise ValueError('{}/{} is not a valid date.'.format(v[0], v[1]))
        return v

    daylight_savings: bool = Field(
        default=False,
        description='Boolean to indicate whether daylight savings time is active '
        'on the design day.'
    )


class ASHRAEClearSky(_SkyCondition):
    """Used to specify sky conditions on a design day."""

    type: constr(regex='^ASHRAEClearSky$') = 'ASHRAEClearSky'

    clearness: float = Field(
        ...,
        ge=0,
        le=1.2,
        description='Value between 0 and 1.2 that will get multiplied by the '
        'irradiance to correct for factors like elevation above sea level.'
    )


class ASHRAETau(_SkyCondition):
    """Used to specify sky conditions on a design day."""

    type: constr(regex='^ASHRAETau$') = 'ASHRAETau'

    tau_b: float = Field(
        ...,
        ge=0,
        le=1.2,
        description='Value for the beam optical depth. Typically found in .stat files.'
    )

    tau_d: float = Field(
        ...,
        ge=0,
        le=3,
        description='Value for the diffuse optical depth. Typically found in .stat files.'
    )


class DesignDayTypes(str, Enum):
    summer_design_day = 'SummerDesignDay'
    winter_design_day = 'WinterDesignDay'
    sunday = 'Sunday'
    monday = 'Monday'
    tuesday = 'Tuesday'
    wednesday = 'Wednesday'
    thursday = 'Thursday'
    friday = 'Friday'
    holiday = 'Holiday'
    custom_day1 = 'CustomDay1'
    custom_day2 = 'CustomDay2'


class DesignDay(NoExtraBaseModel):
    """An object representing design day conditions."""

    type: constr(regex='^DesignDay$') = 'DesignDay'

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='Text string for a unique design day name. This name remains '
        'constant as the object is mutated, copied, and serialized to different '
        'formats (eg. dict, idf, osm). It is also used to reference the object '
        'within SimulationParameters. It must be < 100 characters, use only '
        'ASCII characters and exclude (, ; ! \\n \\t).'
    )

    @validator('name')
    def check_identifier(cls, v):
        assert all(ord(i) < 128 for i in v), 'Name contains non ASCII characters.'
        assert all(char not in v for char in (',', ';', '!', '\n', '\t')), \
            'Name contains an invalid character for EnergyPlus (, ; ! \\n \\t).'
        return v

    day_type: DesignDayTypes

    dry_bulb_condition: DryBulbCondition = Field(
        ...,
        description='A DryBulbCondition describing temperature conditions on '
        'the design day.'
    )

    humidity_condition: HumidityCondition = Field(
        ...,
        description='A HumidityCondition describing humidity and precipitation '
        'conditions on the design day.'
    )

    wind_condition: WindCondition = Field(
        ...,
        description='A WindCondition describing wind conditions on the design day.'
    )

    sky_condition: Union[ASHRAEClearSky, ASHRAETau]
